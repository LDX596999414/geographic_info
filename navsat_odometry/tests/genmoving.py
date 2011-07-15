#!/usr/bin/python
#
#  Navigation satellite odometry test data generator script.
#
#
# $Id$ 

PKG_NAME = 'navsat_odometry'

import math

# ROS node setup
import roslib;
roslib.load_manifest(PKG_NAME)
import rospy

# ROS messages
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix

def test(hz):
    "run test at specified frequency"

    gps_pub = rospy.Publisher('gps', NavSatFix)
    imu_pub = rospy.Publisher('imu', Imu)

    fix = NavSatFix()
    fix.header.frame_id = "/odom"

    # set position at University of Texas, Austin, Pickle Research Campus
    fix.latitude = 30.385315
    fix.longitude = -97.728524

    # set covariance matrix to known, artificial values
    fix.position_covariance_type = NavSatFix.COVARIANCE_TYPE_KNOWN
    fix.position_covariance[0] = 00.0
    fix.position_covariance[1] = 01.0
    fix.position_covariance[2] = 02.0
    fix.position_covariance[3] = 10.0
    fix.position_covariance[4] = 11.0
    fix.position_covariance[5] = 12.0
    fix.position_covariance[6] = 20.0
    fix.position_covariance[7] = 21.0
    fix.position_covariance[8] = 22.0

    # set IMU not moving
    imu = Imu()
    imu.header.frame_id = "/base_link"
    imu.orientation.w = 1.0

    # set IMU covariance matrices to known, artificial values
    imu.orientation_covariance[0] = 33.0
    imu.orientation_covariance[1] = 34.0
    imu.orientation_covariance[2] = 35.0
    imu.orientation_covariance[3] = 43.0
    imu.orientation_covariance[4] = 44.0
    imu.orientation_covariance[5] = 45.0
    imu.orientation_covariance[6] = 53.0
    imu.orientation_covariance[7] = 54.0
    imu.orientation_covariance[8] = 55.0
    imu.angular_velocity_covariance[0] = 33.0
    imu.angular_velocity_covariance[1] = 34.0
    imu.angular_velocity_covariance[2] = 35.0
    imu.angular_velocity_covariance[3] = 43.0
    imu.angular_velocity_covariance[4] = 44.0
    imu.angular_velocity_covariance[5] = 45.0
    imu.angular_velocity_covariance[6] = 53.0
    imu.angular_velocity_covariance[7] = 54.0
    imu.angular_velocity_covariance[8] = 55.0

    deltaDeg = 0.000001
    deltaYaw = 0.01
    yaw = 0.0

    while not rospy.is_shutdown():

        # stagger publication of the two topics
        fix.header.stamp = rospy.Time.now()

        if yaw >= math.pi:
            yaw = -math.pi
        yaw += deltaYaw

        fix.latitude += deltaDeg * math.cos(yaw);
        fix.longitude += deltaDeg * math.sin(yaw);
        fix.altitude = 100.0 + yaw;
        gps_pub.publish(fix)
        rospy.sleep(0.5/hz)

        imu.header.stamp = fix.header.stamp
        # TODO adjust orientation
        imu_pub.publish(imu)
        rospy.sleep(0.5/hz)

if __name__ == '__main__':
    rospy.init_node('genstatic')
    rospy.loginfo('starting static navsat_odometry test')
    try:
        test(20.0)
    except rospy.ROSInterruptException: pass

    rospy.loginfo('static navsat_odometry test completed')
