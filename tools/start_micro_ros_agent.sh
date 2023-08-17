source /opt/ros/noetic/setup.bash
rosparam load bridge.yaml
docker run -v /dev:/dev --privileged -it --rm --net=host microros/micro-ros-agent:foxy serial --dev /dev/ttyACM1
