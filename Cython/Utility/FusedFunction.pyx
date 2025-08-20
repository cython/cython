#################### match_signatures ####################

cimport cython


@cname("__pyx_ff_build_signature_index")
cdef list build_signature_index(signatures: dict, fused_sigindex_ref: list):
    cdef dict sigindex_node

    fused_sigindex = {}
    for sig in signatures:
        sigindex_node = fused_sigindex
        *sig_series, last_type = (<str> sig).strip('()').split('|')
        for sig_type in sig_series:
            if sig_type not in sigindex_node:
                sigindex_node[sig_type] = sigindex_node = {}
            else:
                sigindex_node = <dict> sigindex_node[sig_type]
        sigindex_node[last_type] = sig

    # We always use it as list in "match_signatures()", so wrap it directly.
    index_list = [fused_sigindex]
    fused_sigindex_ref[0] = index_list  # cache in single-item list
    return index_list


@cname("__pyx_ff_match_signatures")
cdef object match_signatures(signatures: dict, dest_sig: list, sigindex_candidates: list):
    sigindex_matches = []

    for dst_type in dest_sig:
        found_matches = []
        found_candidates = []

        # Make two separate lists:
        # One for signature sub-trees with at least one definite match,
        # and another for signature sub-trees with only ambiguous matches
        # (where `dest_sig[i] is None`).
        if dst_type is None:
            for sn in sigindex_matches:
                found_matches.extend((<dict> sn).values())
            for sn in sigindex_candidates:
                found_candidates.extend((<dict> sn).values())
        else:
            for sn in sigindex_matches:
                type_match = (<dict> sn).get(dst_type)
                if type_match is not None:
                    found_matches.append(type_match)
            for sn in sigindex_candidates:
                type_match = (<dict> sn).get(dst_type)
                if type_match is not None:
                    found_matches.append(type_match)

        sigindex_matches = found_matches
        sigindex_candidates = found_candidates

        if not (found_candidates or found_matches):
            break

    match_count = len(sigindex_matches)
    if match_count != 1:
        raise TypeError("Function call with ambiguous argument types" if match_count else "No matching signature found")

    return signatures[ sigindex_matches[0] ]
