===========
SPI
===========

简介
=====
串行外设接口（Serial Peripheral Interface Bus，SPI）是一种用于短程通信的同步串行通信接口规范，设备之间使用全双工模式通信，是一个主机和一个或多个从机的主从模式。
SPI使用4根线完成全双工的通信，这4根信号线分别是：CS（片选）、SCLK（时钟）、MOSI(主机输出从机输入)、MISO(主机输入从机输出)。

主要特征
=========
- 既可作为SPI主设备，也可作为SPI从设备
- 主从设备都支持4种工作模式（CPOL，CPHA）
- 主从设备都支持1/2/3/4字节传输模式
- 发送和接收通道各有深度为32个字节的FIFO
- 自适应的FIFO深度变化特性，适配高性能的应用场景

     + 当Frame为32Bits时，FIFO的深度为8
     + 当Frame为24Bits时，FIFO的深度为8
     + 当Frame为16Bits时，FIFO的深度为16
     + 当Frame为8Bits时，FIFO的深度为32

- 可调整每个Frame的字节传输顺序
- 可配置每个字节内的MSB/LSB优先传输
- 灵活的时钟配置，最高可支持80M时钟
- 接收忽略功能，可以忽略对每个Frame指定位置数据的接收
- 支持从设备模式下的超时机制
- 支持DMA传输模式

功能描述
===========
基本架构
-------------
.. figure:: ../../picture/SPIFramework.svg
   :align: center

   SPI基本架构图

时序控制
-------------
依照不同的时钟极性和相位设定，SPI时钟共有四种模式，可以通过寄存器spi_config的cr_spi_sclk_pol（CPOL）和cr_spi_sclk_ph（CPHA）进行设置。
CPOL用来决定SCK时钟信号空闲时的电平，CPOL=0(cr_spi_sclk_pol=0)则空闲电平为低电平，CPOL=1(cr_spi_sclk_pol=1)则空闲电平为高电平。
CPHA用来决定采样时刻，CPHA=0(cr_spi_sclk_ph=1)则在每个周期的第一个时钟沿采样，CPHA=1(cr_spi_sclk_ph=0)则在每个周期的第二个时钟沿采样。
通过设置寄存器spi_prd_0和spi_prd_1，还可以调整时钟的开始和结束电平持续时间、每个周期内相位0/1的时间以及每帧数据之间的间隔。四种模式下的具体设置如下图所示：

.. figure:: ../../picture/SPIClock.svg
   :align: center

   SPI时序图

其中各数字含义如下：

 - 1是起始条件的长度，通过寄存器spi_prd_0中的cr_spi_prd_s进行配置。
 - 2是停止条件的长度，通过寄存器spi_prd_0中的cr_spi_prd_p进行配置。
 - 3是相位0的长度，通过寄存器spi_prd_0中的cr_spi_prd_d_ph_0进行配置。
 - 4是相位1的长度，通过寄存器spi_prd_0中的cr_spi_prd_d_ph_1进行配置。
 - 5是每帧数据之间的间隔，通过寄存器spi_prd_1中的cr_spi_prd_i进行配置。


主设备连续传输模式
-------------------
开启该模式后，在发送完当前数据帧后 TX FIFO 里还存在待发送数据时，CS信号不会被拉高。

主从设备数据收发
---------------------
通过寄存器 spi_config 中的 cr_spi_frame_size 可以设置数据收发时的 framesize（8/16/24/32-bit），主从设备应保持相同的 framesize。
如果主设备和从设备约定以 32bits 的 framesize 进行通信，在某一帧数据中，主设备的 clk 由于异常不满足 32 个周期时，会出现下列现象：

- 主设备当前发送的这帧数据不会进入从设备的 RX FIFO 中，而是被丢弃，从设备当前发送的数据也不会进入主设备的 RX FIFO 中。
- 从设备会认为当前数据帧已经发送结束，等下次主设备 clk 正常，继续发送下一帧数据。

接收忽略功能
-------------
通过设置忽略的开始位和结束位，SPI 会将接收的每帧数据中的对应数据段丢弃。如下图所示：

.. figure:: ../../picture/SPIIgnore.svg
   :align: center

   SPI Ignore波形图

通过配置寄存器 spi_config 中的 cr_spi_rxd_ignr_en 开启忽略功能。通过配置寄存器 spi_rxd_ignr 中的 cr_spi_rxd_ignr_s 设置忽略功能的起始位。通过配置寄存器 spi_rxd_ignr 中的 cr_spi_rxd_ignr_p 设置忽略功能的结束位。

如上图所示，如果忽略的开始位设为 0，结束位设为 7 则 Dummy Byte 会被收到，结束位设为 15 则 Dummy Byte 会被丢弃。

滤波功能
----------------
通过使能该功能和设置门限值，SPI 会将小于或等于门限值宽度的数据过滤。假设SPI top clock 为 160MHz，门限值设为4，则宽度在（4/160MHz = 25ns）以下的数据都会被过滤掉。
该功能由寄存器 spi_config 中的 cr_spi_deg_en 进行使能，通过配置 cr_spi_deg_cnt 可以设置门限值。
滤波过程如下图所示，假设 cr_spi_deg_cnt 的值设置为4，input为初始数据，output为滤波后的数据。

滤波逻辑过程：

 - tgl为input和output的异或结果。
 - deg_cnt从0开始计数，计数条件为tgl为高电平，并且reached为低电平。
 - 若deg_cnt计数值达到cr_urx_deg_cnt设置的值时，reached为高电平。
 - 当reached为高电平时，将input输出到output。
 - 注释:deg_cnt自加的条件：tgl为高电平且reached为低电平，其余情况下deg_cnt会被清0。

.. figure:: ../../picture/SPIDeg.svg
   :align: center

   SPI滤波波形图

可调整字节传输顺序
--------------------
该功能仅限于调整每一帧数据内不同的 byte 间的优先传输顺序。通过配置寄存器 spi_config 中的 cr_spi_byte_inv 位进行设置。0 表示优先发送低字节，1 表示优先发送高字节。
以 frame size 等于 24 bits 传输数据为例，数据格式为：Data[23:0]=0x123456。
当设置优先发送低字节，传输的顺序为：0x56(第1个字节：低字节)；0x34(第2个字节：中间字节)；0x12(第3个字节：高字节)；
当设置优先发送高字节，传输的顺序为：0x12(第3个字节：高字节)；0x34(第2个字节：中间字节)；0x56(第1个字节：低字节)；

字节传输顺序调整功能可以和 MSB/LSB 传输配置功能配合使用。

可配置每个字节的 MSB/LSB 优先传输
-------------------------------------
该功能仅限于设置每个 byte 中的 8 个 bits 间的优先传输顺序，通过配置寄存器 spi_config 中的 cr_spi_bit_inv 位进行设置。0 表示 MSB-First，1 表示 LSB-First。
同样以 frame size 等于 24 bits 传输数据为例，数据格式为：Data[23:0]=0x123456。

当设置为 MSB-First 传输时，传输的顺序为：01010110(二进制，第1个字节：0x56);00110100(二进制，第2个字节：0x34);00010010(二进制，第3个字节：0x12)；

当设置为 LSB-First 传输时，传输的顺序为：01101010(二进制，第1个字节：0x56);00101100(二进制，第2个字节：0x34);01001000(二进制，第3个字节：0x12)。

从模式超时机制
--------------------------------
通过寄存器 spi_sto_value 可以设定超时门限值，当 SPI 处于从模式且检测到CS被拉低时，会开始计时，如果超过了该超时门限所对应的时间仍未收到时钟信号时，会触发超时中断。

I/O传输模式
-------------
CPU 可以响应来自 FIFO 的中断来执行 FIFO 填充和清空操作。每个 FIFO 都有一个可编程的 FIFO 触发阈值来触发中断。
当寄存器 spi_fifo_config_1 中的 rx_fifo_cnt 大于 rx_fifo_th 触发阈值时，将产生 RX 请求中断，通知 CPU 读取 RX FIFO 中的数据。
当寄存器 spi_fifo_config_1 中的 tx_fifo_cnt 大于 tx_fifo_th 时，将产生 TX 请求中断，通知 CPU 向 TX FIFO 填充数据。
可以通过查询 FIFO 状态寄存器来确定 FIFO 中的采样值以及 FIFO 的状态。
需要确保正确的 RX FIFO 触发阈值和 TX FIFO 触发阈值，以防止 FIFO overflow 或 underflow。

DMA 传输模式
-------------
SPI 支持 DMA 传输模式。使用该模式需要分别设置 TX 和 RX FIFO 的阈值，将寄存器 spi_fifo_config_0 中的 spi_dma_tx_en 置 1，则开启 DMA 发送模式。
将寄存器 spi_fifo_config_0 中的 spi_dma_rx_en 置 1，则开启 DMA 接收模式。
当该模式启用后，SPI 会对 TX/RX FIFO 进行检查，一旦寄存器 spi_fifo_config_1 中的 tx_fifo_cnt/rx_fifo_cnt 大于 tx_fifo_th/rx_fifo_th，
将会发起 DMA 请求，DMA 会按照设定将数据搬移至 TX FIFO 中或从 RX FIFO 中移出。

SPI 中断
-------------
SPI 有着丰富的中断控制，包括以下几种中断模式：

- SPI 传输结束中断

  * 在主模式下，SPI 传输结束中断会在每帧数据传输结束时触发。
  * 在从模式下，SPI 传输结束中断会在 CS 信号被拉高时触发。

- TX FIFO 请求中断

  * TX FIFO 请求中断会在其 FIFO 可用计数值大于设定的阈值时触发，当条件不满足时该中断标志会自动清除。

- RX FIFO 请求中断

  * RX FIFO 请求中断会在其 FIFO 可用计数值大于设定的阈值时触发，当条件不满足时该中断标志会自动清除。

- 从模式传输超时中断
  
  * 从模式传输超时中断会在从模式下检测到CS拉低之后，超过超时门限值对应的时间后仍未收到时钟信号时触发。

- 从模式 TX 过载中断
  
  * 从模式 TX 过载中断会在从模式下 TX 没有准备好数据传输而时钟信号却已经到来时触发。

- TX/RX FIFO 溢出中断

  * 如果 TX/RX FIFO 发生了上溢或者下溢，会触发 TX/RX FIFO 溢出中断，当 FIFO 清除寄存器 spi_fifo_config_0 中的 tx_fifo_clr/rx_fifo_clr 被置 1 时，对应的 FIFO 会被清空，同时溢出中断标志会自动清除。

可通过寄存器 SPI_INT_STS 查询各中断状态和对相应的位写 1 清除中断。

.. only:: html

   .. include:: spi_register.rst

.. raw:: latex

   \input{../../zh_CN/content/spi}