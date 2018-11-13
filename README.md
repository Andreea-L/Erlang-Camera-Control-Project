# Real-time Robot Camera Control in Erlang
Software Engineering BSc Final Project

The research done as part of this project also contributed to the publishing of the following paper:
[Andreea Lutac, Natalia Chechina, Gerardo Aragon-Camarasa, and Phil Trinder. 2016. Towards reliable and scalable robot communication. In Proceedings of the 15th International Workshop on Erlang (Erlang 2016). ACM, New York, NY, USA, 12-23. DOI: http://dx.doi.org/10.1145/2975969.2975971](https://dl.acm.org/citation.cfm?id=2975971)

This dissertation investigates the applicability of Erlang as an alternative robot control system software architecture
that may improve upon the scalability and reliability limitations of more traditional approaches based
on the Robot Operating System (ROS). Literature examining Erlang in the context of robotics has identified its
potential within the field of robotic control, but has so far failed to employ concrete metrics to quantify the nonfunctional
advantages of Erlang. The project bridges this research gap by performing a comparative analysis of
the scalability and reliability of two typical robotic middlewares relying on ROS and Erlang, respectively.


Using a controllable camera as a typical robotic component, two face tracking systems were developed that apply
ROS and Erlang-based asynchronous message passing models to achieve communication between a camera
device and associated face detection worker processes. To verify the hypothesis of Erlang offering improved
performance, a suite of five experiments was carried out on both applications. 

The first three of these trials targeted scalability and their findings indicated that Erlang is capable of supporting **3.5 times** more active processes
than ROS, at a generally similar communication latency of approximately **37 ms** for a camera-process-camera
roundtrip and no decline in face quality. In addition, Erlang exhibited **2.2 times** lower per-process memory costs
when compared to the ROS system. The latter two experiments tackled the reliability of the face tracking architectures
and illustrated that, while both systems are able to successfully recover from partial crashes, Erlang
is able to restart failed processed approximately **1000 to 1500 times** faster than the ROS services and therefore
better mitigate the impact on the quality of tracking.


The implications of these results provide credence to the original arguments and highlight the favourable prospects
of Erlang in robotics. The project concludes that, if applied appropriately and accessed through optimised linking
libraries, an Erlang-based middleware possesses the potential to greatly improve the flexibility and availability
of large-scale robotic systems.
