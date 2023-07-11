powershell 是 通用的， 但是 PostMessageA 是 windows的函数

@REM BOOL PostMessageA(
@REM   [in, optional] HWND   hWnd,
@REM   [in]           UINT   Msg,
@REM   [in]           WPARAM wParam,
@REM   [in]           LPARAM lParam
@REM );

@REM SC_MONITORPOWER 0xF170
@REM 设置显示的状态。 此命令支持具有节能功能的设备，例如电池供电的个人计算机。
@REM     lParam 参数可以具有以下值：
@REM     -1 (显示器打开)
@REM     1 (显示器将进入低功耗)
@REM     2 (显示器正在关闭)

@REM 动动鼠标、键盘就亮了
powershell (Add-Type '[DllImport(\"user32.dll\")]^public static extern int PostMessage(int hWnd, int hMsg, int wParam, int lParam);' -Name a -Pas)::PostMessage(-1,0x0112,0xF170,2)

