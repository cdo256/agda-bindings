(defun agda-export-symbols (filename)
  "Export Agda input method translations to CSV, handling multi-character entries."
  (interactive "FOutput file: ")
  (require 'agda-input)
  (with-temp-buffer
    (insert "Sequence,Character,Hex\n")
    (dolist (entry agda-input-translations)
      (let* ((seq (concat "\\" (car entry)))
             (chars (cdr entry))
             (hex (lambda (c) 
                    (ignore-errors 
                      (format "U+%04X" (string-to-char c)))))
             (counter 1))
        (cond
         ((listp chars)  ; Handle list case
          (dolist (c chars)
            (insert (format "\"%s\",%s,%s,%d\n" seq c (funcall hex c) counter))
            (setq counter (+ counter 1))))
         ((stringp chars)  ; Handle single character
          (insert (format "\"%s\",%s,%s,1\n" seq chars (funcall hex chars)))))))
    (write-region (point-min) (point-max) filename))
  (message "Exported Agda symbols to %s" filename))

(agda-export-symbols "bindings.csv")
