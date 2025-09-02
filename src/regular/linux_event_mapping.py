def get_event_mapping():
    """
    提供Linux专用的事件映射列表，包含Syslog设施中文映射及常见事件属性
    字段说明：
    - event_id: 事件唯一标识（自定义格式：进程-事件类型）
    - event_type: 事件业务类型（如登录认证、服务管理）
    - log_category: Syslog设施（facility）英文名称
    - log_category_cn: Syslog设施中文名称
    - log_source: 事件来源进程（如sshd、sudo、kernel）
    - level: 事件级别（英文，符合Syslog标准）
    - level_cn: 事件级别中文名称
    - description: 事件描述（英文）
    - description_cn: 事件描述（中文）
    返回：list[dict] - 结构化的Linux事件映射数据
    """
    # -------------------------- Linux Syslog设施（facility）中英文映射表 --------------------------
    syslog_facility_map = {
        'auth': {'cn': '认证相关'},
        'authpriv': {'cn': '私密认证'},
        'cron': {'cn': '定时任务'},
        'daemon': {'cn': '系统守护进程'},
        'kern': {'cn': '内核消息'},
        'lpr': {'cn': '打印服务'},
        'mail': {'cn': '邮件服务'},
        'mark': {'cn': '时间标记'},
        'news': {'cn': '新闻组'},
        'security': {'cn': '安全事件'},
        'syslog': {'cn': '系统日志'},
        'user': {'cn': '用户级消息'},
        'uucp': {'cn': 'UUCP服务'},
        'local0': {'cn': '本地设施0'},
        'local1': {'cn': '本地设施1'},
        'local2': {'cn': '本地设施2'},
        'local3': {'cn': '本地设施3'},
        'local4': {'cn': '本地设施4'},
        'local5': {'cn': '本地设施5'},
        'local6': {'cn': '本地设施6'},
        'local7': {'cn': '本地设施7'}
    }

    # -------------------------- 核心事件映射列表 --------------------------
    return [
        # 1. 认证类事件（auth/authpriv设施）
        {
            "event_id": "sshd-success",
            "event_type": "登录认证",
            "log_category": "authpriv",
            "log_category_cn": syslog_facility_map['authpriv']['cn'],
            "log_source": "sshd",
            "level": "Information",
            "level_cn": "信息",
            "description": "Successful SSH login (password authentication)",
            "description_cn": "SSH登录成功（密码认证）"
        },
        {
            "event_id": "sshd-failure",
            "event_type": "登录认证",
            "log_category": "authpriv",
            "log_category_cn": syslog_facility_map['authpriv']['cn'],
            "log_source": "sshd",
            "level": "Warning",
            "level_cn": "警告",
            "description": "Failed SSH login attempt (invalid password)",
            "description_cn": "SSH登录尝试失败（密码无效）"
        },
        {
            "event_id": "sudo-success",
            "event_type": "权限提升",
            "log_category": "auth",
            "log_category_cn": syslog_facility_map['auth']['cn'],
            "log_source": "sudo",
            "level": "Information",
            "level_cn": "信息",
            "description": "Successful sudo command execution (user: root)",
            "description_cn": "sudo命令执行成功（目标用户：root）"
        },
        {
            "event_id": "sudo-failure",
            "event_type": "权限提升",
            "log_category": "auth",
            "log_category_cn": syslog_facility_map['auth']['cn'],
            "log_source": "sudo",
            "level": "Error",
            "level_cn": "错误",
            "description": "Failed sudo authentication (user: non-root)",
            "description_cn": "sudo认证失败（非root用户）"
        },

        # 2. 内核类事件（kern设施）
        {
            "event_id": "kernel-usb-error",
            "event_type": "硬件事件",
            "log_category": "kern",
            "log_category_cn": syslog_facility_map['kern']['cn'],
            "log_source": "kernel",
            "level": "Error",
            "level_cn": "错误",
            "description": "USB device initialization error (error code: -71)",
            "description_cn": "USB设备初始化错误（错误码：-71）"
        },
        {
            "event_id": "kernel-disk-warning",
            "event_type": "存储事件",
            "log_category": "kern",
            "log_category_cn": syslog_facility_map['kern']['cn'],
            "log_source": "kernel",
            "level": "Warning",
            "level_cn": "警告",
            "description": "Disk I/O error detected (device: /dev/sda1)",
            "description_cn": "检测到磁盘I/O错误（设备：/dev/sda1）"
        },
        {
            "event_id": "kernel-network-up",
            "event_type": "网络事件",
            "log_category": "kern",
            "log_category_cn": syslog_facility_map['kern']['cn'],
            "log_source": "kernel",
            "level": "Information",
            "level_cn": "信息",
            "description": "Network interface up (eth0: 192.168.1.100)",
            "description_cn": "网络接口启用（eth0：192.168.1.100）"
        },

        # 3. 定时任务事件（cron设施）
        {
            "event_id": "cron-exec-success",
            "event_type": "定时任务",
            "log_category": "cron",
            "log_category_cn": syslog_facility_map['cron']['cn'],
            "log_source": "CRON",
            "level": "Information",
            "level_cn": "信息",
            "description": "Cron job executed (path: /etc/cron.hourly)",
            "description_cn": "定时任务执行成功（路径：/etc/cron.hourly）"
        },
        {
            "event_id": "cron-exec-failure",
            "event_type": "定时任务",
            "log_category": "cron",
            "log_category_cn": syslog_facility_map['cron']['cn'],
            "log_source": "CRON",
            "level": "Error",
            "level_cn": "错误",
            "description": "Cron job failed (script: /home/user/backup.sh)",
            "description_cn": "定时任务执行失败（脚本：/home/user/backup.sh）"
        },

        # 4. 守护进程事件（daemon设施）
        {
            "event_id": "systemd-start",
            "event_type": "服务管理",
            "log_category": "daemon",
            "log_category_cn": syslog_facility_map['daemon']['cn'],
            "log_source": "systemd",
            "level": "Information",
            "level_cn": "信息",
            "description": "Service started (name: nginx, PID: 1234)",
            "description_cn": "服务启动成功（名称：nginx，进程ID：1234）"
        },
        {
            "event_id": "systemd-crash",
            "event_type": "服务管理",
            "log_category": "daemon",
            "log_category_cn": syslog_facility_map['daemon']['cn'],
            "log_source": "systemd",
            "level": "Error",
            "level_cn": "错误",
            "description": "Service crashed (name: mysql, exit code: 1)",
            "description_cn": "服务崩溃（名称：mysql，退出码：1）"
        },

        # 5. 防火墙事件（syslog设施）
        {
            "event_id": "firewalld-block",
            "event_type": "防火墙",
            "log_category": "syslog",
            "log_category_cn": syslog_facility_map['syslog']['cn'],
            "log_source": "firewalld",
            "level": "Information",
            "level_cn": "信息",
            "description": "Connection blocked (source: 10.0.0.5, port: 8080)",
            "description_cn": "连接被防火墙阻止（来源：10.0.0.5，端口：8080）"
        },
        {
            "event_id": "firewalld-allow",
            "event_type": "防火墙",
            "log_category": "syslog",
            "log_category_cn": syslog_facility_map['syslog']['cn'],
            "log_source": "firewalld",
            "level": "Information",
            "level_cn": "信息",
            "description": "Connection allowed (source: 192.168.1.0/24, port: 22)",
            "description_cn": "连接被防火墙允许（来源：192.168.1.0/24，端口：22）"
        },

        # 6. 本地设施事件（local0-local7）
        {
            "event_id": "app-log-local0",
            "event_type": "应用日志",
            "log_category": "local0",
            "log_category_cn": syslog_facility_map['local0']['cn'],
            "log_source": "app-server",
            "level": "Information",
            "level_cn": "信息",
            "description": "Application started (version: 2.1.0)",
            "description_cn": "应用启动成功（版本：2.1.0）"
        }
    ]


