
(cl:in-package :asdf)

(defsystem "rosorbitcamera-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Int32Numpy" :depends-on ("_package_Int32Numpy"))
    (:file "_package_Int32Numpy" :depends-on ("_package"))
  ))