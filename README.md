# XJTU-RMV-Task04

## 多线程
> 对于实时帧率的获取以及断连的检测，二者都是持续性的过程，如果放在主线程中将会很大程度上占用主线程，可能造成很大的延迟等问题，因此选择把实时帧率的获取和断连检测各开一个线程
```cpp
std::thread grab_thread_;

grab_thread_ = std::thread([this]() {//这个this作用就是传入指针，让线程内的语句可以访问线程外的变量。
    // ⬇️ 这个 lambda 表达式就是线程要执行的任务
    while (rclcpp::ok()) {
        //在线程中通过无限循环来不断获取帧率。
        ...
    }
});
```

> 断开重连
```cpp
        reconnect_thread_ = std::thread([this]() {
            rclcpp::Rate rate(1.0);  // 每秒检测一次
            while (rclcpp::ok())
            {
                while(!connected_ && rclcpp::ok())
                {
                    if (tryReconnect())
                    {
                        RCLCPP_INFO(this->get_logger(), "相机重连成功！");
                        break;
                    }
                }
                rate.sleep();
            }
        });
```
![](./photos/duanxian)
![](./photos/chonglian)




## 实时帧率获取
> 使用的是海康官方函数接口
```cpp
MVCC_FLOATVALUE fps_value = {0};
int nRet = MV_CC_GetFloatValue(handle_, "ResultingFrameRate", &fps_value);
if (nRet == MV_OK) {
    float fps = static_cast<float>(fps_value.fCurValue);
    std_msgs::msg::Float32 fps_msg;
    fps_msg.data = fps;
    fps_pub_->publish(fps_msg);
    RCLCPP_INFO(this->get_logger(), "硬件实际帧率: %.2f FPS", fps);
} 
```
使用的多线程，故可以实时获得实际帧率，修改后也可同步更新
![](./photos/frame_rate)
**值得注意的是，获取的实时最高帧率只能到65.46，暂时不知道什么原因，也许是因为相机的缘故....**

## 回调函数
> 在特定事件发生时，会自动调用提前注册好的函数

## 参数更新
**支持使用ros2的param系统对参数进行更新**
可更新的参数包括：
1. 帧率
2. 曝光时间
3. 增益
4. 图像格式
![](./photos/params)
![](./photos/frate_c)
