; Auto-generated. Do not edit!


(cl:in-package rosorbitcamera-msg)


;//! \htmlinclude Int32Numpy.msg.html

(cl:defclass <Int32Numpy> (roslisp-msg-protocol:ros-message)
  ((data
    :reader data
    :initarg :data
    :type (cl:vector cl:integer)
   :initform (cl:make-array 0 :element-type 'cl:integer :initial-element 0)))
)

(cl:defclass Int32Numpy (<Int32Numpy>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Int32Numpy>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Int32Numpy)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rosorbitcamera-msg:<Int32Numpy> is deprecated: use rosorbitcamera-msg:Int32Numpy instead.")))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <Int32Numpy>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rosorbitcamera-msg:data-val is deprecated.  Use rosorbitcamera-msg:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Int32Numpy>) ostream)
  "Serializes a message object of type '<Int32Numpy>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'data))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    ))
   (cl:slot-value msg 'data))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Int32Numpy>) istream)
  "Deserializes a message object of type '<Int32Numpy>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'data) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'data)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296)))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Int32Numpy>)))
  "Returns string type for a message object of type '<Int32Numpy>"
  "rosorbitcamera/Int32Numpy")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Int32Numpy)))
  "Returns string type for a message object of type 'Int32Numpy"
  "rosorbitcamera/Int32Numpy")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Int32Numpy>)))
  "Returns md5sum for a message object of type '<Int32Numpy>"
  "563b27884d008b0d2adff54dc1f9e4f5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Int32Numpy)))
  "Returns md5sum for a message object of type 'Int32Numpy"
  "563b27884d008b0d2adff54dc1f9e4f5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Int32Numpy>)))
  "Returns full string definition for message of type '<Int32Numpy>"
  (cl:format cl:nil "int32[] data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Int32Numpy)))
  "Returns full string definition for message of type 'Int32Numpy"
  (cl:format cl:nil "int32[] data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Int32Numpy>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'data) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Int32Numpy>))
  "Converts a ROS message object to a list"
  (cl:list 'Int32Numpy
    (cl:cons ':data (data msg))
))
