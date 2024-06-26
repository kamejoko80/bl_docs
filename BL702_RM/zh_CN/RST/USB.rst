===========
USB
===========

简介
=====
USB(Universal Serial Bus)通用串行总线，完全支持USB1.1全速设备，对USB2.0部分支持。

主要特征
=========
- 支持USB full speed device-mode

- 支持8个双向端点：EP0可配置为控制/批量/中断/同步端点，EP1-EP7可配置为批量/中断/同步端点

- 每个端点均包含TX、RX两个方向的FIFO，FIFO深度64字节，并且支持DMA

- 支持内部transceiver

- 支持suspend/resume

- 支持LPM

- 支持多种USB中断配置

功能描述
===========
USB使用步骤
--------------

1.配置内部transceiver，寄存器在0x40000228和0x4000022C

2.配置usb_config及各个端点的epx_config

3.配置USB中断相关寄存器

4.配置USB DMA相关（可选）

5.配置GPIO为USB功能（内部transceiver----function为10）

6.置一0x40000228[20]usb_enum以触发主机端枚举流程

部分寄存器配置及功能描述
-------------------------------

- swrdy:只读，仅当此位为0时，才可以向cr_usb_ep0_sw_rdy写入1
- crsr:写1自动清零，当软件允许下一包回复ACK时向此域写1，则仅下一包会回复ACK，对于OUT/IN事务数据会收入FIFO/从FIFO发出（FIFO放行一次）
- e0snko:需要置一，代表OUT事务会默认回复NAK，数据不会进入FIFO（FIFO不放行）
- e0snki:需要置一，代表IN事务会默认回复NAK，数据不会从FIFO发出（FIFO不放行）
- e0ss:写1自动清零，当软件允许下一包回复STALL时向此域写1，则仅下一包会回复STALL
- epxdit:“令牌包 => 触发xxx_cmd_int => 数据包 => 触发xxx_done_int => 握手包”
- epxcit:“令牌包 => 触发xxx_cmd_int => 数据包 => 触发xxx_done_int => 握手包”
- ep0odit:“令牌包 => 触发xxx_cmd_int => 数据包 => 触发xxx_done_int => 握手包”
- ep0ocit:“令牌包 => 触发xxx_cmd_int => 数据包 => 触发xxx_done_int => 握手包”
- ep0idit:“令牌包 => 触发xxx_cmd_int => 数据包 => 触发xxx_done_int => 握手包”
- ep0icit:“令牌包 => 触发xxx_cmd_int => 数据包 => 触发xxx_done_int => 握手包”
- ep0sdit:“令牌包 => 触发xxx_cmd_int => 数据包 => 触发xxx_done_int => 握手包”
- ep0scit:“令牌包 => 触发xxx_cmd_int => 数据包 => 触发xxx_done_int => 握手包”
- exrs:只读，仅当此位为0时，才可以向cr_epx_rdy写入1
- exr:写1自动清零，当软件允许下一包回复ACK时向此域写1，则仅下一包会回复ACK（FIFO放行一次）
- exn:需要置一，代表事务会默认回复NAK，IN/OUT取决于当前端点的传输方向配置（FIFO不放行）
- exs:当软件希望挂起此端点时置一，置一后此端点永远只回复STALL

.. figure:: ../../picture/USBIT.svg
   :align: center
   :scale: 70%

   USB中断触发方式

USB枚举阶段中断处理流程
--------------------------

1.首先是10ms以上的reset，会触发reset中断。

2.当reset结束时，会触发reset end中断。

3.枚举过程的SETUP事务、IN事务、OUT事务会分别触发e0sdit、e0icit、ep0dit。

4.枚举结束后，主机与特定端点EPx之间的IN事务、OUT事务会分别触发epxcit、epxdit。


各传输事务的寄存器操作流程
----------------------------------

- 控制传输——SETUP事务数据接收：
    * 进入中断
    * 判断e0sdit中断标志位
    * e0rfr内存放的就是setup事务所传来的数据，根据e0rfc读取e0rfr即可获得
    * 置一crsr以放行后续事务
    * 清除中断标志位
    * 退出中断

- 控制传输——IN事务数据发送：
    * 进入中断
    * 判断e0idit中断标志位
    * 等待swrdy为0时才可以向e0tfw内写入数据
    * 置一crsr以放行后续事务
    * 清除中断标志位
    * 退出中断

- 控制传输——OUT事务数据接收：
    * 进入中断
    * 判断ep0dit中断标志位
    * e0rfr内存放的就是OUT事务所传来的数据，根据e0rfc读取e0rfr即可获得
    * 置一crsr以放行后续事务
    * 清除中断标志位
    * 退出中断

- EPx(x=1...7)——IN事务数据发送：
    * 进入中断
    * 判断epxcit中断标志位
    * 等待exrs为0时才可以向extfw内写入数据（仅当只发送1个字节时，exs需要修改为1）
    * 置一exr以放行后续事务
    * 清除中断标志位
    * 退出中断

- EPx(x=1...7)——OUT事务数据接收：
    * 进入中断
    * 判断epxdit中断标志位
    * exrfr内存放的就是OUT事务所传来的数据，根据exrfc读取exrfr即可获得
    * 置一exrs以放行后续事务
    * 清除中断标志位
    * 退出中断

.. figure:: ../../picture/USBCommunicate.svg
   :align: center
   :scale: 70%

   USB通信方式

内部transceiver寄存器推荐配置：

.. table:: 寄存器配置1

    +---------------------+-----------+
    |      usb_xcvr       |   value   |
    +=====================+===========+
    | usb_rcv             | read only |
    +---------------------+-----------+
    | usb_vip             | read only |
    +---------------------+-----------+
    | usb_vim             | read only |
    +---------------------+-----------+
    | usb_bd              | read only |
    +---------------------+-----------+
    | pu_usb              |    0->1   |
    +---------------------+-----------+
    | usb_sus             |     0     |
    +---------------------+-----------+
    | usb_spd             |     1     |
    +---------------------+-----------+
    | usb_enum            |    0->1   |
    +---------------------+-----------+
    | usb_data_convert    |     0     |
    +---------------------+-----------+
    | usb_oeb             | read only |
    +---------------------+-----------+
    | usb_oeb_reg         |     1     |
    +---------------------+-----------+
    | usb_oeb_sel         |     0     |
    +---------------------+-----------+
    | usb_rout_pmos       |     3     |
    +---------------------+-----------+
    | usb_rout_nmos       |     3     |
    +---------------------+-----------+
    | pu_usb_ldo          |     0     |
    +---------------------+-----------+
    | usb_ldo_vfb         |     3     |
    +---------------------+-----------+

.. table:: 寄存器配置2

    +---------------------+-----------+
    |   usb_xcvr_config   |   value   |
    +=====================+===========+
    | usb_slewrate_p_rise |     4     |
    +---------------------+-----------+
    | usb_slewrate_p_fall |     3     |
    +---------------------+-----------+
    | usb_slewrate_m_rise |     4     |
    +---------------------+-----------+
    | usb_slewrate_m_fall |     3     |
    +---------------------+-----------+
    | usb_res_pullup_tune |     2     |
    +---------------------+-----------+
    | reg_usb_use_ctrl    |     0     |
    +---------------------+-----------+
    | usb_str_drv         |     1     |
    +---------------------+-----------+
    | reg_usb_use_xcvr    |     1     |
    +---------------------+-----------+
    | usb_bd_vth          |     7     |
    +---------------------+-----------+
    | usb_v_hys_p         |     1     |
    +---------------------+-----------+
    | usb_v_hys_m         |     1     |
    +---------------------+-----------+

注意：当准备开启内部transceiver时需要将pu_usb和usb_enum置一。

.. only:: html

   .. include:: usb_register.rst

.. raw:: latex

   \input{../../zh_CN/content/usb}