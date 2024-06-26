==========
TIMER
==========

简介
=====
芯片内置两个32-bit定时器，定时器可独立控制并配置其参数与时钟频率。

芯片内有一个 Watchdog 定时器，不可预知的软件或硬件行为可能导致应用程序工作失常，Watchdog 定时器可以帮助系统从中恢复。如果当前阶段超过预定时间，
仍没有喂狗或关闭 Watchdog 定时器，会触发中断或系统复位。

.. figure:: ../../picture/TimerBlock.svg
   :align: center

   定时器框图

.. figure:: ../../picture/WatchdogBlock.svg
   :align: center

   Watchdog 定时器框图

主要特征
=========
- 32-bit 定时器

   * 多种时钟来源，最高可支持80M时钟
   * 8-bit时钟分频器，分频系数为1-256
   * 两个32-bit定时器
   * 定时器包含三组触发阈值设定，达到阈值时触发中断
   * 支持 FreeRun 模式和 Preload 模式
   * 支持测量外部 GPIO 的脉冲宽度

- Watchdog 定时器

   * 一个 16-bit Watchdog 定时器
   * 支持写保护，防止误设定造成系统异常
   * 支持中断或复位两种方式


功能描述
==========

5 种 Watchdog 定时器时钟，可通过寄存器 TCCR 中的 cs_wdt 选择：

- BCLK--总线时钟
- 32K--32K时钟
- 1K--1K时钟（32K的分频）
- XTAL--外部晶振
- GPIO--外部GPIO

5 种 timer 定时器时钟，可通过寄存器 TCCR 中的 cs_2 和 cs_3 选择：

- BCLK--总线时钟
- 32K--32K时钟
- 1K--1K时钟（32K的分频）
- XTAL--外部晶振
- GPIO--外部GPIO

定时器有各自的8-bit分频器，通过寄存器 TCDR 中的tcdr2、tcdr3、wcdr配置，
可对其选择的时钟源进行1-256的分频。
设定为0时表示不分频，设定为1时表示2分频以此类推，
最大分频系数为256，定时器以分频后的时钟作为计数周期单位。


通用定时器工作原理
--------------------

通用定时器包含三组比较器，一个计数器以及一个预加载寄存器，当设定好时钟源，
启动定时器后，计数器从初始值开始向上累加计数，当计数器的值与比较器相等的时候，
比较寄存器置位的同时产生比较中断。


寄存器 TICR2 中的 tclr2_0 设置 timer0 比较器0的值，寄存器 TICR2 中的 tclr2_1 设置 timer0 比较器1的值，
寄存器 TICR2 中的 tclr2_2 设置 timer0 比较器2的值。寄存器 TPLVR2 中的 tplvr2 设置 timer0 预加载值。

寄存器 TICR3 中的 tclr3_0 设置 timer1 比较器0的值，寄存器 TICR3 中的 tclr3_1 设置 timer1 比较器1的值，
寄存器 TICR3 中的 tclr3_2 设置 timer1 比较器2的值。寄存器 TPLVR3 中的 tplvr3 设置 timer1 预加载值。


定时器支持两种计数模式： PreLoad 模式和 FreeRun 模式，通过寄存器 TCMR 配置。
寄存器 TCMR 中的 timer2_mode 设置 timer0 的计数模式，寄存器 TCMR 中的 timer3_mode 设置 timer1 的计数模式。


PreLoad模式
^^^^^^^^^^^
PreLoad模式下计数器的初始值为 TPLVR 寄存器（预加载寄存器）的值，从这个初始值开始向上累加计数。
寄存器 TPLVR2 设置 timer0 的 Preload 预加载值，寄存器 TPLVR3 配置 timer1 的 Preload 预加载值。
寄存器 TPLCR2 中的 tplcr2 配置 timer0 的 PreLoad 触发条件， 寄存器 TPLCR3 中的 tplcr3 配置 timer1 的 PreLoad 触发条件。
当满足 PreLoad 触发条件时，计数器的值会被重新置为 PreLoad 寄存器的值，然后计数器再次开始向上累加计数。


在定时器的计数器计数过程中，一旦计数器的值与三个比较器中的某比较值一致，
该比较器的比较标志就会置位，并可以产生相应的比较中断。


若预加载寄存器的值为10，比较器0的值为13，比较器1的值为16，比较器2的值为19，
则定时器在PreLoad的模式下工作时序如下图：

.. figure:: ../../picture/TimerPreload.svg
   :align: center

   定时器在PreLoad模式下工作时序

FreeRun模式
^^^^^^^^^^^
FreeRun模式即计数器累加模式，在 FreeRun 模式下计数器的初始值为0，在启动定时器后从0开始累加计数，
当达到计数最大值后，再次从0开始计数。

在定时器的计数器计数过程中，一旦计数器的值与三个比较器中的某比较值一致，
该比较器的比较标志就会置位，并可以产生相应的比较中断。

在FreeRun模式下，定时器工作时序与PreLoad基本相同，
只是计数器会从0开始累计到最大值，期间产生的比较标志和比较中断的机制与PreLoad模式相同。


测量外部GPIO脉冲宽度
^^^^^^^^^^^^^^^^^^^^
定时器支持使用内部时钟源计算外部GPIO的脉冲宽度。

配置的步骤如下：

1. 将外部 GPIO 配置成 gpio_tmr_clk 功能。通过配置GLB模块中寄存器dig_clk_cfg2实现。

   寄存器 dig_clk_cfg2[13:12] 位为 gpio_tmr_clk_sel: 选择GPIO clock模式；
   寄存器 dig_clk_cfg2[11:8] 中的某一位配置为0，表示 clock input 模式。
   这两个寄存器需要配套使用，配置方法如下，根据使用的GPIO以此类推。

.. table:: gpio_tmr_clk 功能配置
    :widths: 20,40,40
    :width: 100%
    :align: center

    +-------------+----------------------------------+----------------------------------------+
    |    GPIO     | dig_clk_cfg2[13:12]              | dig_clk_cfg2[11:8]                     |
    +=============+==================================+========================================+
    |    GPIO0    | gpio_tmr_clk = 0                 | chip_clk_out_0_en = 0                  |
    +-------------+----------------------------------+----------------------------------------+
    |    GPIO1    | gpio_tmr_clk = 1                 | chip_clk_out_1_en = 0                  |
    +-------------+----------------------------------+----------------------------------------+
    |    GPIO2    | gpio_tmr_clk = 2                 | chip_clk_out_2_en = 0                  |
    +-------------+----------------------------------+----------------------------------------+
    |    GPIO3    | gpio_tmr_clk = 3                 | chip_clk_out_3_en = 0                  |
    +-------------+----------------------------------+----------------------------------------+
    |    GPIO4    | gpio_tmr_clk = 0                 | chip_clk_out_0_en = 0                  |
    +-------------+----------------------------------+----------------------------------------+

2. 寄存器 GPIO 中的 timer2_gpio_inv / timer3_gpio_inv 位配置需要测量外部脉宽的高电平还是低电平。
   如果该位为0，表示高电平；该位为1表示低电平。

3. 配置寄存器 GPIO 中的 timer2_gpio_en 使能 GPIO 测量功能

4. 配置定时器时钟源和运行模式，并使能timer

5. 当寄存器 GPIO 中的 gpio_lat_ok 置1后，获取寄存器 GPIO_LAT2 和寄存器 GPIO_LAT1 的值并计算宽度

外部 GPIO 的脉冲宽度的计算方式：（ GPIO_LAT2 - GPIO_LAT1 ）\* timer内部时钟源的1个周期的宽度；

例如：timer的内部时钟源为80M，外部 GPIO 的频率为2M，占空比为1：1，计算外部 GPIO 低电平和高电平的宽度。

- 将timer2_gpio_inv位写1，表示计算外部gpio低电平的宽度。按照上述配置完成后，得到寄存器 GPIO_LAT2 和寄存器 GPIO_LAT1 的差为20，则外部gpio的低电平宽度为：20 \*（1 / 80000000） = 1 / 4000000。
- 将timer2_gpio_inv位写0，表示计算外部gpio高电平的宽度。按照上述配置完成后，如果寄存器 GPIO_LAT2 和寄存器 GPIO_LAT1 的差为20，则外部gpio的低电平宽度为：20 \*（1 / 80000000） = 1 / 4000000。

Watchdog 定时器工作原理
----------------------
Watchdog 定时器包含一个计数器和一个比较器，计数器从0开始累加计数，
如果计数器被复位(喂狗)，则从0再次开始向上计数，当计数器的值与比较器相等的时候，
可以产生一个比较中断信号或者系统复位信号，用户可以根据需要选择使用其中一个。
Watchdog 计数器会在每个计数周期单位上加1，软件可以在任何时间点通过 APB 将 Watchdog 计数器归零。

Watchdog 定时器通过寄存器 WMR 中的 wmr 设置比较值，若比较值为6，Watchdog 的工作时序如下图所示:

.. figure:: ../../picture/WatchDog.svg
   :align: center

   Watchdog 工作时序

定时器 Alarm 设定
-----------------
计数器有三个比较值提供软件设定，并可设定比较值是否触发 alarm 中断，
当计数器达到比较值且设定会 alarm 时，计数器通过中断通知处理器。
软件可以通过 APB 读取目前是否发生 alarm 和是哪个比较值触发 alarm 中断，
当清理 alarm 中断时亦会同步清理 alarm 状态。

Watchdog Alarm 设定
-----------
Watchdog 可设定一组比较值，当软件因为系统错误，来不及将 Watchdog 计数器归零，
导致 Watchdog 计数器超过比较值时，便会触发 Watchdog alarm ，alarm 方式有两种，
第一种是通过中断通知软件进行必要的处置，第二种是进入系统 Watchdog 复位。
Watchdog 复位被触发时，会通知系统复位控制器，并做好系统复位前准备，
当一切就绪后进入系统 Watchdog 复位，且软件可通过 APB 读取 WSR
寄存器得知是否曾经发生过 Watchdog 系统复位。

.. figure:: ../../picture/WatchDogAlarm.svg
   :align: center

   Watchdog alarm 机制

.. only:: html

   .. include:: tmr_register.rst

.. raw:: latex

   \input{../../zh_CN/content/tmr}