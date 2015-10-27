;; Auto-generated. Do not edit!


(when (boundp 'rosorbitcamera::Int32Numpy)
  (if (not (find-package "ROSORBITCAMERA"))
    (make-package "ROSORBITCAMERA"))
  (shadow 'Int32Numpy (find-package "ROSORBITCAMERA")))
(unless (find-package "ROSORBITCAMERA::INT32NUMPY")
  (make-package "ROSORBITCAMERA::INT32NUMPY"))

(in-package "ROS")
;;//! \htmlinclude Int32Numpy.msg.html


(defclass rosorbitcamera::Int32Numpy
  :super ros::object
  :slots (_data ))

(defmethod rosorbitcamera::Int32Numpy
  (:init
   (&key
    ((:data __data) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _data __data)
   self)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:serialization-length
   ()
   (+
    ;; int32[] _data
    (* 4    (length _data)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32[] _data
     (write-long (length _data) s)
     (dotimes (i (length _data))
       (write-long (elt _data i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32[] _data
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _data (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _data i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get rosorbitcamera::Int32Numpy :md5sum-) "563b27884d008b0d2adff54dc1f9e4f5")
(setf (get rosorbitcamera::Int32Numpy :datatype-) "rosorbitcamera/Int32Numpy")
(setf (get rosorbitcamera::Int32Numpy :definition-)
      "int32[] data

")



(provide :rosorbitcamera/Int32Numpy "563b27884d008b0d2adff54dc1f9e4f5")


