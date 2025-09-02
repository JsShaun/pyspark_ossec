
def get_event_mapping():
    """创建包含事件类型的完整事件ID映射关系"""
    return [
        # 系统事件 - 启动/关机
        {
            "event_id": "6005",
            "event_type": "系统启动/关机",
            "log_category": "System",
            "log_source": "EventLog",
            "level": "Information",
            "level_cn": "信息",
            "description": "The Event log service was started.",
            "description_cn": "事件日志服务已启动。"
        },
        {
            "event_id": "6006",
            "event_type": "系统启动/关机",
            "log_category": "System",
            "log_source": "EventLog",
            "level": "Information",
            "level_cn": "信息",
            "description": "The Event log service was stopped.",
            "description_cn": "事件日志服务已停止。"
        },
        {
            "event_id": "6008",
            "event_type": "系统启动/关机",
            "log_category": "System",
            "log_source": "EventLog",
            "level": "Error",
            "level_cn": "错误",
            "description": "The previous system shutdown was unexpected.",
            "description_cn": "上一次系统 shutdown 是意外的。"
        },
        
        # 系统事件 - 服务管理
        {
            "event_id": "7000",
            "event_type": "服务管理",
            "log_category": "System",
            "log_source": "Service Control Manager",
            "level": "Error",
            "level_cn": "错误",
            "description": "A service failed to start.",
            "description_cn": "服务启动失败。"
        },
        {
            "event_id": "7001",
            "event_type": "服务管理",
            "log_category": "System",
            "log_source": "Service Control Manager",
            "level": "Error",
            "level_cn": "错误",
            "description": "A service depends on another service that failed to start.",
            "description_cn": "服务依赖于未能启动的另一个服务。"
        },
        {
            "event_id": "7036",
            "event_type": "服务管理",
            "log_category": "System",
            "log_source": "Service Control Manager",
            "level": "Information",
            "level_cn": "信息",
            "description": "A service entered the running state.",
            "description_cn": "服务已进入运行状态。"
        },
        {
            "event_id": "7035",
            "event_type": "服务管理",
            "log_category": "System",
            "log_source": "Service Control Manager",
            "level": "Information",
            "level_cn": "信息",
            "description": "A service was successfully sent a start control.",
            "description_cn": "服务成功接收启动控制。"
        },
        
        # 系统事件 - 驱动程序
        {
            "event_id": "219",
            "event_type": "驱动程序",
            "log_category": "System",
            "log_source": "Microsoft-Windows-Kernel-PnP",
            "level": "Warning",
            "level_cn": "警告",
            "description": "Driver failed to load for a device.",
            "description_cn": "设备驱动程序加载失败。"
        },
        {
            "event_id": "10000",
            "event_type": "驱动程序",
            "log_category": "System",
            "log_source": "Microsoft-Windows-DriverFrameworks-UserMode",
            "level": "Error",
            "level_cn": "错误",
            "description": "Driver failed to initialize.",
            "description_cn": "驱动程序初始化失败。"
        },
        
        # 安全事件 - 登录/注销
        {
            "event_id": "4624",
            "event_type": "登录/注销",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "An account was successfully logged on.",
            "description_cn": "账户登录成功。"
        },
        {
            "event_id": "4625",
            "event_type": "登录/注销",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "An account failed to log on.",
            "description_cn": "账户登录失败。"
        },
        {
            "event_id": "4634",
            "event_type": "登录/注销",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "An account was logged off.",
            "description_cn": "账户已注销。"
        },
        {
            "event_id": "4647",
            "event_type": "登录/注销",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "User initiated logoff.",
            "description_cn": "用户主动注销。"
        },
        
        # 安全事件 - 账户管理
        {
            "event_id": "4720",
            "event_type": "账户管理",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "A user account was created.",
            "description_cn": "用户账户已创建。"
        },
        {
            "event_id": "4722",
            "event_type": "账户管理",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "A user account was enabled.",
            "description_cn": "用户账户已启用。"
        },
        {
            "event_id": "4725",
            "event_type": "账户管理",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "A user account was disabled.",
            "description_cn": "用户账户已禁用。"
        },
        {
            "event_id": "4726",
            "event_type": "账户管理",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "A user account was deleted.",
            "description_cn": "用户账户已删除。"
        },
        {
            "event_id": "4740",
            "event_type": "账户管理",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "A user account was locked out.",
            "description_cn": "用户账户已被锁定。"
        },
        
        # 安全事件 - 进程管理
        {
            "event_id": "4688",
            "event_type": "进程管理",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "A new process has been created.",
            "description_cn": "已创建新进程。"
        },
        {
            "event_id": "4689",
            "event_type": "进程管理",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "A process has exited.",
            "description_cn": "进程已退出。"
        },
        {
            "event_id": "4698",
            "event_type": "进程管理",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "A scheduled task was created.",
            "description_cn": "已创建计划任务。"
        },
        
        # 安全事件 - 权限变更
        {
            "event_id": "4672",
            "event_type": "权限变更",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "Special privileges assigned to new logon.",
            "description_cn": "已为新登录分配特殊权限。"
        },
        {
            "event_id": "4673",
            "event_type": "权限变更",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "A privileged service was called.",
            "description_cn": "已调用特权服务。"
        },
        
        # 应用程序事件 - 应用错误
        {
            "event_id": "1000",
            "event_type": "应用错误",
            "log_category": "Application",
            "log_source": "Application Error",
            "level": "Error",
            "level_cn": "错误",
            "description": "Faulting application error.",
            "description_cn": "应用程序出错。"
        },
        {
            "event_id": "1001",
            "event_type": "应用错误",
            "log_category": "Application",
            "log_source": "Application Error",
            "level": "Information",
            "level_cn": "信息",
            "description": "Fault bucket, type 0.",
            "description_cn": "错误存储桶，类型 0。"
        },
        {
            "event_id": "1002",
            "event_type": "应用错误",
            "log_category": "Application",
            "log_source": "Application Hang",
            "level": "Error",
            "level_cn": "错误",
            "description": "A program stopped interacting with Windows.",
            "description_cn": "程序停止与Windows交互。"
        },
        
        # 应用程序事件 - .NET运行时
        {
            "event_id": "1026",
            "event_type": ".NET运行时",
            "log_category": "Application",
            "log_source": ".NET Runtime",
            "level": "Error",
            "level_cn": "错误",
            "description": "Application: .NET Runtime exception.",
            "description_cn": "应用程序：.NET运行时异常。"
        },
        
        # 硬件事件
        {
            "event_id": "20001",
            "event_type": "硬件设备",
            "log_category": "Microsoft-Windows-Hardware-DeviceInstallation/Admin",
            "log_source": "Microsoft-Windows-Hardware-DeviceInstallation",
            "level": "Information",
            "level_cn": "信息",
            "description": "A device was installed successfully.",
            "description_cn": "设备安装成功。"
        },
        {
            "event_id": "20003",
            "event_type": "硬件设备",
            "log_category": "Microsoft-Windows-Hardware-DeviceInstallation/Admin",
            "log_source": "Microsoft-Windows-Hardware-DeviceInstallation",
            "level": "Error",
            "level_cn": "错误",
            "description": "A device installation failed.",
            "description_cn": "设备安装失败。"
        },
        {
            "event_id": "1234",
            "event_type": "硬件错误",
            "log_category": "System",
            "log_source": "Microsoft-Windows-WHEA-Logger",
            "level": "Critical",
            "level_cn": "严重",
            "description": "A fatal hardware error has occurred.",
            "description_cn": "发生致命硬件错误。"
        },
        
        # 网络事件 - 防火墙
        {
            "event_id": "2004",
            "event_type": "防火墙",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Windows Firewall With Advanced Security",
            "level": "Information",
            "level_cn": "信息",
            "description": "A Windows Firewall setting has changed.",
            "description_cn": "Windows防火墙设置已更改。"
        },
        {
            "event_id": "5156",
            "event_type": "防火墙",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "A packet was allowed through the firewall.",
            "description_cn": "数据包已通过防火墙。"
        },
        {
            "event_id": "5157",
            "event_type": "防火墙",
            "log_category": "Security",
            "log_source": "Microsoft-Windows-Security-Auditing",
            "level": "Information",
            "level_cn": "信息",
            "description": "A packet was blocked by the firewall.",
            "description_cn": "数据包被防火墙阻止。"
        },
        
        # 网络事件 - 远程桌面
        {
            "event_id": "1149",
            "event_type": "远程桌面",
            "log_category": "System",
            "log_source": "Microsoft-Windows-TerminalServices-RemoteConnectionManager",
            "level": "Information",
            "level_cn": "信息",
            "description": "User authentication succeeded for remote connection.",
            "description_cn": "远程连接的用户身份验证成功。"
        },
        {
            "event_id": "24",
            "event_type": "远程桌面",
            "log_category": "System",
            "log_source": "Microsoft-Windows-TerminalServices-LocalSessionManager",
            "level": "Information",
            "level_cn": "信息",
            "description": "Remote session connected.",
            "description_cn": "远程会话已连接。"
        },
        
        # 更新与补丁
        {
            "event_id": "19",
            "event_type": "系统更新",
            "log_category": "System",
            "log_source": "Microsoft-Windows-WindowsUpdateClient",
            "level": "Information",
            "level_cn": "信息",
            "description": "Windows update installed successfully.",
            "description_cn": "Windows更新安装成功。"
        },
        {
            "event_id": "20",
            "event_type": "系统更新",
            "log_category": "System",
            "log_source": "Microsoft-Windows-WindowsUpdateClient",
            "level": "Error",
            "level_cn": "错误",
            "description": "Windows update failed to install.",
            "description_cn": "Windows更新安装失败。"
        },
        
        # 组策略
        {
            "event_id": "1501",
            "event_type": "组策略",
            "log_category": "System",
            "log_source": "Microsoft-Windows-GroupPolicy",
            "level": "Information",
            "level_cn": "信息",
            "description": "Group Policy settings were processed successfully.",
            "description_cn": "组策略设置已成功处理。"
        },
        {
            "event_id": "1058",
            "event_type": "组策略",
            "log_category": "System",
            "log_source": "Microsoft-Windows-GroupPolicy",
            "level": "Error",
            "level_cn": "错误",
            "description": "Group Policy failed to process.",
            "description_cn": "组策略处理失败。"
        }
    ]
    



