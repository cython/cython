;; Cython mode

;; Load python-mode if available, otherwise use builtin emacs python package
(when (not(require 'python-mode nil t))
  (require 'python))

(add-to-list 'auto-mode-alist '("\\.pyx\\'" . cython-mode))
(add-to-list 'auto-mode-alist '("\\.pxd\\'" . cython-mode))
(add-to-list 'auto-mode-alist '("\\.pxi\\'" . cython-mode))


(defun cython-compile ()
  "Compile the file via Cython."
  (interactive)
  (let ((cy-buffer (current-buffer)))
    (with-current-buffer
        (compile compile-command)
      (set (make-local-variable 'cython-buffer) cy-buffer)
      (add-to-list (make-local-variable 'compilation-finish-functions)
                   'cython-compilation-finish)))
  )

(defun cython-compilation-finish (buffer how)
  "Called when Cython compilation finishes."
  ;; XXX could annotate source here
  )

(defvar cython-mode-map
  (let ((map (make-sparse-keymap)))
    ;; Will inherit from `python-mode-map' thanks to define-derived-mode.
    (define-key map "\C-c\C-c" 'cython-compile)
    map)
  "Keymap used in `cython-mode'.")

(defvar cython-font-lock-keywords
  `(;; new keywords in Cython language
    (,(regexp-opt '("by" "cdef" "cimport" "cpdef" "ctypedef" "enum" "except?"
                    "extern" "gil" "include" "nogil" "property" "public"
                    "readonly" "struct" "union" "DEF" "IF" "ELIF" "ELSE") 'words)
     1 font-lock-keyword-face)
    ;; C and Python types (highlight as builtins)
    (,(regexp-opt '("NULL" "bint" "char" "dict" "double" "float" "int" "list"
                    "long" "object" "Py_ssize_t" "short" "size_t" "void") 'words)
     1 font-lock-builtin-face)
    ;; cdef is used for more than functions, so simply highlighting the next
    ;; word is problematic. struct, enum and property work though.
    ("\\<\\(?:struct\\|enum\\)[ \t]+\\([a-zA-Z_]+[a-zA-Z0-9_]*\\)"
     1 py-class-name-face)
    ("\\<property[ \t]+\\([a-zA-Z_]+[a-zA-Z0-9_]*\\)"
     1 font-lock-function-name-face))
  "Additional font lock keywords for Cython mode.")

(define-derived-mode cython-mode python-mode "Cython"
  "Major mode for Cython development, derived from Python mode.

\\{cython-mode-map}"
  (setcar font-lock-defaults
          (append python-font-lock-keywords cython-font-lock-keywords))
  (set (make-local-variable 'compile-command)
       (concat "cython -a " buffer-file-name))
  (add-to-list (make-local-variable 'compilation-finish-functions)
               'cython-compilation-finish)
)

(provide 'cython-mode)
