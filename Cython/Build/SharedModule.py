import os

from Cython.Compiler import (
    MemoryView, Code, Options, Pipeline, Errors, Main, Symtab
)
from Cython.Compiler.StringEncoding import EncodedString
from Cython.Compiler.Scanning import SharedUtilitySourceDescriptor
from Cython.Compiler.Errors import warning


def list_of_features(included=None, excluded=None, _list_of_features=[]):
    if _list_of_features:
        feature_names = _list_of_features[:]
    else:
        feature_names = sorted({feature_name for feature_name, _, _ in _iter_exports()})
        _list_of_features[:] = feature_names

    return _select_features(feature_names, included, excluded)


def _select_features(all_names, included, excluded):
    names = all_names
    if included:
        included = set(included)
        unknown = included.difference(all_names)
        if unknown:
            warning(None, f"Unknown shared module features selected: {', '.join(sorted(unknown))}")

        names = [name for name in names if name in included]

    if excluded:
        excluded = set(excluded)
        unknown = excluded.difference(all_names)
        if unknown:
            warning(None, f"Unknown shared module features excluded: {', '.join(sorted(unknown))}")
        unused = excluded.difference(names)
        if unused:
            warning(None, f"Shared module features excluded that was not included: {', '.join(sorted(unused))}")

        names = [name for name in names if name not in excluded]

    return names


def _iter_exports(selected_features=None):
    UtilityCode = Code.UtilityCode
    match_special = UtilityCode.get_special_comment_matcher('/')

    for c_utility_file in os.listdir(Code.get_utility_dir()):
        if not c_utility_file.endswith('.c'):
            continue

        file_base_name = os.path.splitext(os.path.basename(c_utility_file))[0]
        current_feature_name = file_base_name.partition('_')[0]

        current_section = None
        for line in Code.read_utilities_hook(c_utility_file):
            if '//' not in line or not line.startswith('//'):
                continue
            match = match_special(line)
            if match is None:
                continue

            name = match.group('name')
            if name:
                if current_section:
                    if selected_features is None or current_section[0] in selected_features:
                        yield current_section
                current_section = None

                section_title = UtilityCode.match_section_title(name) if '.export' in name else None
                if section_title:
                    name, section_type = section_title.groups()
                    if section_type == 'export':
                        current_section = [current_feature_name, name, c_utility_file]

            elif (tag := match.group('tag')) and tag.startswith('feature') and current_section:
                explicit_feature_name = tag.split(':', 1)[-1].strip()
                assert current_section[0] == current_feature_name, (
                    "Conflicting feature names given to the same utility code section: "
                    f"{current_section[0]!r} and {explicit_feature_name!r}")
                current_section[0] = explicit_feature_name

        if current_section:
            if selected_features is None or current_section[0] in selected_features:
                yield current_section


def create_shared_library_pipeline(context, scope, options, result, selected_features=None):

    parse = Pipeline.parse_stage_factory(context)

    def generate_tree_factory(context):
        def generate_tree(compsrc):
            tree = parse(compsrc)

            if selected_features is None or 'MemoryView' in selected_features:
                tree.scope.use_utility_code(
                    MemoryView.get_view_utility_code(options.shared_utility_qualified_name))

                tree.scope.use_utility_code(MemoryView._get_memviewslice_declare_code())
                tree.scope.use_utility_code(MemoryView._get_typeinfo_to_format_code())

            context.include_directories.append(Code.get_utility_dir())
            return tree

        return generate_tree

    def generate_c_utilities(module_node):
        UtilityCode = Code.UtilityCode
        for _, name, c_utility_file in _iter_exports(selected_features):
            module_node.scope.use_utility_code(UtilityCode.load_cached(name, c_utility_file))
        return module_node

    orig_cimport_from_pyx = Options.cimport_from_pyx

    def set_cimport_from_pyx(cimport_from_pyx):
        def inner(node):
            Options.cimport_from_pyx = cimport_from_pyx
            return node
        return inner

    return [
        # "cimport_from_pyx=True" to force generating __Pyx_ExportFunction
        set_cimport_from_pyx(True),
        generate_tree_factory(context),
        *Pipeline.create_pipeline(context, 'pyx', exclude_classes=()),
        generate_c_utilities,
        Pipeline.inject_pxd_code_stage_factory(context),
        Pipeline.inject_utility_code_stage_factory(context, internalise_c_class_entries=False),
        Pipeline.inject_utility_pxd_code_stage_factory(context),
        Pipeline.abort_on_errors,
        Pipeline.generate_pyx_code_stage_factory(options, result),
        set_cimport_from_pyx(orig_cimport_from_pyx),
    ]


def generate_shared_module(options):
    Errors.reset()

    dest_c_file = options.shared_c_file_path
    pyx_file = os.path.splitext(dest_c_file)[0] + '.pyx'
    module_name = os.path.splitext(os.path.basename(dest_c_file))[0]

    selected_features = None
    if options.shared_utility_features_enabled or options.shared_utility_features_disabled:
        selected_features = list_of_features(
            options.shared_utility_features_enabled,
            options.shared_utility_features_disabled,
        )

    context = Main.Context.from_options(options)
    scope = Symtab.ModuleScope('MemoryView', parent_module = None, context = context, is_package=False)

    source_desc = SharedUtilitySourceDescriptor(pyx_file)
    comp_src = Main.CompilationSource(source_desc, EncodedString(module_name), os.getcwd())
    result = Main.create_default_resultobj(comp_src, options)

    pipeline = create_shared_library_pipeline(
        context, scope, options, result,
        selected_features=selected_features,
    )
    err, enddata = Pipeline.run_pipeline(pipeline, comp_src)

    return err, enddata
