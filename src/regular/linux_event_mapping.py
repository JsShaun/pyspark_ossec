def get_event_mapping():
    """创建包含事件类型的完整事件ID映射关系，所有规则支持忽略大小写匹配"""
    return [
    # SSH相关事件
    {
        "program": "sshd",
        "event_id": "sshd_auth_success_pwd",
        "event_cn": "SSH密码认证成功",
        "regex": "(?i)sshd\\[\\d+\\]: Accepted password for (\\S+) from (\\S+)",
        "event_type": "authentication",
        "log_category": "security",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "sshd",
        "event_id": "sshd_auth_fail_pwd",
        "event_cn": "SSH密码认证失败",
        "regex": "(?i)sshd\\[\\d+\\]: Failed password for (invalid user )?(\\S+) from (\\S+)",
        "event_type": "authentication_failure",
        "log_category": "security",
        "level": 3,
        "level_cn": "中"
    },
    {
        "program": "sshd",
        "event_id": "sshd_auth_success_key",
        "event_cn": "SSH公钥认证成功",
        "regex": "(?i)sshd\\[\\d+\\]: Accepted publickey for (\\S+) from (\\S+)",
        "event_type": "authentication",
        "log_category": "security",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "sshd",
        "event_id": "sshd_invalid_user",
        "event_cn": "SSH尝试无效用户登录",
        "regex": "(?i)sshd\\[\\d+\\]: Invalid user (\\S+) from (\\S+)",
        "event_type": "authentication_failure",
        "log_category": "security",
        "level": 4,
        "level_cn": "中高"
    },
    {
        "program": "sshd",
        "event_id": "sshd_conn_closed",
        "event_cn": "SSH连接被关闭",
        "regex": "(?i)sshd\\[\\d+\\]: Connection closed by (authenticated user \\S+ | \\S+)",
        "event_type": "connection",
        "log_category": "system",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "sshd",
        "event_id": "sshd_too_many_fails",
        "event_cn": "SSH多次认证失败",
        "regex": "(?i)sshd\\[\\d+\\]: Too many authentication failures for (\\S+)",
        "event_type": "brute_force_attempt",
        "log_category": "security",
        "level": 6,
        "level_cn": "高"
    },
    {
        "program": "sshd",
        "event_id": "sshd_service_start",
        "event_cn": "SSH服务启动",
        "regex": "(?i)sshd\\[\\d+\\]: Server listening on (\\S+) port (\\d+)",
        "event_type": "service_start",
        "log_category": "system",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "sshd",
        "event_id": "sshd_service_stop",
        "event_cn": "SSH服务停止",
        "regex": "(?i)sshd\\[\\d+\\]: Received signal (\\d+); terminating",
        "event_type": "service_stop",
        "log_category": "system",
        "level": 2,
        "level_cn": "中低"
    },

    # Sudo相关事件
    {
        "program": "sudo",
        "event_id": "sudo_session_open",
        "event_cn": "Sudo会话开启",
        "regex": "(?i)sudo\\[\\d+\\]: (\\S+) : TTY=\\S+ ; PWD=.* ; USER=(\\S+) ; COMMAND=.*",
        "event_type": "privilege_escalation",
        "log_category": "security",
        "level": 2,
        "level_cn": "中低"
    },
    {
        "program": "sudo",
        "event_id": "sudo_session_close",
        "event_cn": "Sudo会话关闭",
        "regex": "(?i)sudo\\[\\d+\\]: session closed for user (\\S+)",
        "event_type": "privilege_escalation",
        "log_category": "security",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "sudo",
        "event_id": "sudo_incorrect_pwd",
        "event_cn": "Sudo密码错误",
        "regex": "(?i)sudo\\[\\d+\\]: (\\S+) : incorrect password ; TTY=\\S+ ; PWD=.*",
        "event_type": "privilege_escalation_failure",
        "log_category": "security",
        "level": 4,
        "level_cn": "中高"
    },
    {
        "program": "sudo",
        "event_id": "sudo_command_denied",
        "event_cn": "Sudo命令被拒绝",
        "regex": "(?i)sudo\\[\\d+\\]: (\\S+) : command not allowed ; TTY=\\S+ ; PWD=.* ; USER=(\\S+) ; COMMAND=.*",
        "event_type": "privilege_escalation_failure",
        "log_category": "security",
        "level": 5,
        "level_cn": "中高"
    },

    # 内核相关事件
    {
        "program": "kernel",
        "event_id": "kernel_out_of_memory",
        "event_cn": "内核内存不足",
        "regex": "(?i)kernel: Out of memory: Kill process (\\d+) \\((\\S+)\\) score \\d+ or sacrifice child",
        "event_type": "resource_issue",
        "log_category": "system",
        "level": 5,
        "level_cn": "中高"
    },
    {
        "program": "kernel",
        "event_id": "kernel_disk_error",
        "event_cn": "磁盘I/O错误",
        "regex": "(?i)kernel: (\\S+): (I/O error|failed command): (\\S+)",
        "event_type": "hardware_issue",
        "log_category": "system",
        "level": 6,
        "level_cn": "高"
    },
    {
        "program": "kernel",
        "event_id": "kernel_firewall_drop",
        "event_cn": "内核防火墙丢弃数据包",
        "regex": "(?i)kernel: \\[\\d+\\.\\d+\\] (\\S+): IN=(\\S+) OUT=(\\S+) SRC=(\\S+) DST=(\\S+) .* DROP",
        "event_type": "network_block",
        "log_category": "network",
        "level": 2,
        "level_cn": "中低"
    },
    {
        "program": "kernel",
        "event_id": "kernel_new_device",
        "event_cn": "检测到新设备",
        "regex": "(?i)kernel: (\\S+): new (disk|usb device|network interface) (\\S+)",
        "event_type": "hardware_change",
        "log_category": "system",
        "level": 2,
        "level_cn": "中低"
    },

    # 用户管理相关事件
    {
        "program": "useradd",
        "event_id": "useradd_create",
        "event_cn": "创建用户",
        "regex": "(?i)useradd\\[\\d+\\]: new user: name=(\\S+), UID=(\\d+), GID=(\\d+), home=(\\S+)",
        "event_type": "account_management",
        "log_category": "system",
        "level": 2,
        "level_cn": "中低"
    },
    {
        "program": "userdel",
        "event_id": "userdel_remove",
        "event_cn": "删除用户",
        "regex": "(?i)userdel\\[\\d+\\]: delete user '(\\S+)'",
        "event_type": "account_management",
        "log_category": "system",
        "level": 2,
        "level_cn": "中低"
    },
    {
        "program": "passwd",
        "event_id": "passwd_change",
        "event_cn": "修改用户密码",
        "regex": "(?i)passwd\\[\\d+\\]: changing password for user (\\S+)",
        "event_type": "account_management",
        "log_category": "security",
        "level": 2,
        "level_cn": "中低"
    },
    {
        "program": "usermod",
        "event_id": "usermod_modify",
        "event_cn": "修改用户属性",
        "regex": "(?i)usermod\\[\\d+\\]: modify user '(\\S+)'",
        "event_type": "account_management",
        "log_category": "system",
        "level": 2,
        "level_cn": "中低"
    },
    {
        "program": "groupadd",
        "event_id": "groupadd_create",
        "event_cn": "创建用户组",
        "regex": "(?i)groupadd\\[\\d+\\]: new group: name=(\\S+), GID=(\\d+)",
        "event_type": "account_management",
        "log_category": "system",
        "level": 2,
        "level_cn": "中低"
    },

    # 防火墙相关事件
    {
        "program": "iptables",
        "event_id": "iptables_drop_packet",
        "event_cn": "防火墙丢弃数据包",
        "regex": "(?i)iptables\\[\\d+\\]: DROP (IN=(\\S+) )?SRC=(\\S+) (DST=(\\S+) )?(DPT=(\\d+) )?",
        "event_type": "network_block",
        "log_category": "network",
        "level": 2,
        "level_cn": "中低"
    },
    {
        "program": "iptables",
        "event_id": "iptables_accept_packet",
        "event_cn": "防火墙允许数据包",
        "regex": "(?i)iptables\\[\\d+\\]: ACCEPT (IN=(\\S+) )?SRC=(\\S+) (DST=(\\S+) )?(DPT=(\\d+) )?",
        "event_type": "network_allow",
        "log_category": "network",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "firewalld",
        "event_id": "firewalld_rule_change",
        "event_cn": "防火墙规则变更",
        "regex": "(?i)firewalld\\[\\d+\\]: (Adding|Removing) rule '(.*)'",
        "event_type": "configuration_change",
        "log_category": "security",
        "level": 3,
        "level_cn": "中"
    },

    # 系统登录相关事件
    {
        "program": "login",
        "event_id": "login_success",
        "event_cn": "本地登录成功",
        "regex": "(?i)login\\[\\d+\\]: (pam_unix\\(login:session\\): session opened for user (\\S+) by (\\S+)|USER=(\\S+) LOGIN=\\S+)",
        "event_type": "authentication",
        "log_category": "security",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "login",
        "event_id": "login_failure",
        "event_cn": "本地登录失败",
        "regex": "(?i)login\\[\\d+\\]: FAILED LOGIN (\\d+) FROM (\\S+) FOR (\\S+), (Authentication failure|invalid user)",
        "event_type": "authentication_failure",
        "log_category": "security",
        "level": 3,
        "level_cn": "中"
    },
    {
        "program": "systemd-logind",
        "event_id": "session_start",
        "event_cn": "用户会话开始",
        "regex": "(?i)systemd-logind\\[\\d+\\]: New session (\\S+) of user (\\S+)",
        "event_type": "session_management",
        "log_category": "system",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "systemd-logind",
        "event_id": "session_end",
        "event_cn": "用户会话结束",
        "regex": "(?i)systemd-logind\\[\\d+\\]: Removed session (\\S+)",
        "event_type": "session_management",
        "log_category": "system",
        "level": 1,
        "level_cn": "低"
    },

    # 系统服务相关事件
    {
        "program": "systemd",
        "event_id": "service_start",
        "event_cn": "系统服务启动",
        "regex": "(?i)systemd\\[\\d+\\]: Started (\\S+)\\.(service|socket)",
        "event_type": "service_start",
        "log_category": "system",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "systemd",
        "event_id": "service_failed",
        "event_cn": "系统服务启动失败",
        "regex": "(?i)systemd\\[\\d+\\]: (\\S+)\\.(service|socket) failed (with result '\\S+')?",
        "event_type": "service_failure",
        "log_category": "system",
        "level": 5,
        "level_cn": "中高"
    },
    {
        "program": "systemd",
        "event_id": "service_stop",
        "event_cn": "系统服务停止",
        "regex": "(?i)systemd\\[\\d+\\]: Stopped (\\S+)\\.(service|socket)",
        "event_type": "service_stop",
        "log_category": "system",
        "level": 2,
        "level_cn": "中低"
    },

    # 磁盘空间相关事件
    {
        "program": "df",
        "event_id": "disk_space_low",
        "event_cn": "磁盘空间不足",
        "regex": "(?i)df\\[\\d+\\]: (\\S+)\\s+\\d+% full",
        "event_type": "resource_issue",
        "log_category": "system",
        "level": 4,
        "level_cn": "中高"
    },
    {
        "program": "kernel",
        "event_id": "disk_full",
        "event_cn": "磁盘空间满",
        "regex": "(?i)kernel: (\\S+): write failed, filesystem is full",
        "event_type": "resource_issue",
        "log_category": "system",
        "level": 6,
        "level_cn": "高"
    },

    # 安全相关事件
    {
        "program": "auditd",
        "event_id": "audit_rule_change",
        "event_cn": "审计规则变更",
        "regex": "(?i)auditd\\[\\d+\\]: (Adding|Deleting) audit rule '(.*)'",
        "event_type": "security_change",
        "log_category": "security",
        "level": 4,
        "level_cn": "中高"
    },
    {
        "program": "pam_unix",
        "event_id": "password_expire",
        "event_cn": "用户密码过期",
        "regex": "(?i)pam_unix\\(\\S+\\): password for '(\\S+)' will expire in (\\d+) days",
        "event_type": "account_management",
        "log_category": "security",
        "level": 2,
        "level_cn": "中低"
    },
    # 内核USB设备错误（匹配msg3）
    {
        "program": "kernel",
        "event_id": "kernel_usb_error",
        "event_cn": "USB设备错误",
        "regex": "(?i)kernel\\[\\d+\\]: USB device (not accepting address|failed to initialize) (\\d+), error (-\\d+)",
        "event_type": "hardware_issue",
        "log_category": "system",
        "level": 4,
        "level_cn": "中高"
    },
    
    # CRON任务执行（匹配msg4）
    {
        "program": "CRON",
        "event_id": "cron_job_executed",
        "event_cn": "CRON定时任务执行",
        "regex": "(?i)CRON\\[\\d+\\]: \\((\\S+)\\) CMD \\((.*?)\\)",
        "event_type": "scheduled_task",
        "log_category": "system",
        "level": 1,
        "level_cn": "低"
    },
    
    # 防火墙拒绝连接（匹配msg5）
    {
        "program": "firewalld",
        "event_id": "firewalld_reject_packet",
        "event_cn": "防火墙拒绝数据包",
        "regex": ".*firewalld\[\\d+\]: REJECT:.*",
        "event_type": "network_block",
        "log_category": "network",
        "level": 3,
        "level_cn": "中"
    },
        
    # Nginx访问日志（匹配msg6）
    {
        "program": "nginx",
        "event_id": "nginx_request_processed",
        "event_cn": "Nginx处理HTTP请求",
        "regex": r"(?i)nginx\\[\\d+\\]: (\\S+) - - \"(\\S+) (\\S+) (\\S+)\" (\\d+) (\\d+)",
        "event_type": "web_access",
        "log_category": "application",
        "level": 1,
        "level_cn": "低"
    },
    
    # Nginx错误日志补充
    {
        "program": "nginx",
        "event_id": "nginx_error_occurred",
        "event_cn": "Nginx发生错误",
        "regex": "(?i)nginx\\[\\d+\\]: \\S+ \\[error\\] (\\d+)#(\\d+): (.*)",
        "event_type": "application_error",
        "log_category": "application",
        "level": 4,
        "level_cn": "中高"
    },# -------------------------- 新增Web日志规则 --------------------------
    # 1. Nginx 增强规则
    {
        "program": "nginx",
        "event_id": "nginx_static_resource",
        "event_cn": "Nginx静态资源请求",
        "regex": "(?i)nginx\\[\\d+\\]: (\\S+) - - \\[(.*?)\\] \"GET (.*?\\.(js|css|jpg|png|gif)) HTTP/\\d+\\.\\d+\" 200 (\\d+)",
        "event_type": "web_access",
        "log_category": "application",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "nginx",
        "event_id": "nginx_reverse_proxy",
        "event_cn": "Nginx反向代理请求",
        "regex": "(?i)nginx\\[\\d+\\]: (\\S+) - - \\[(.*?)\\] \"(\\S+) (.*?) HTTP/\\d+\\.\\d+\" 200 (\\d+) \"-\" \"(.*?)\" \"(\\S+)\"",
        "event_type": "web_proxy",
        "log_category": "application",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "nginx",
        "event_id": "nginx_sensitive_path",
        "event_cn": "Nginx敏感路径访问",
        "regex": "(?i)nginx\\[\\d+\\]: (\\S+) - - \\[(.*?)\\] \"(\\S+) (/admin|/login|/api|/manage)/.* HTTP/\\d+\\.\\d+\" (\\d+)",
        "event_type": "web_security",
        "log_category": "application",
        "level": 2,
        "level_cn": "中低"
    },
    {
        "program": "nginx",
        "event_id": "nginx_abnormal_status",
        "event_cn": "Nginx异常状态码",
        "regex": "(?i)nginx\\[\\d+\\]: (\\S+) - - \\[(.*?)\\] \"(\\S+) (.*?) HTTP/\\d+\\.\\d+\" (403|404|500|503) (\\d+)",
        "event_type": "web_error",
        "log_category": "application",
        "level": 4,
        "level_cn": "中高"
    },

    # 2. Apache 日志规则
    {
        "program": "apache",
        "event_id": "apache_access",
        "event_cn": "Apache访问日志",
        "regex": "(?i)apache\\[\\d+\\]: (\\S+) - - \\[(.*?)\\] \"(\\S+) (.*?) HTTP/\\d+\\.\\d+\" (\\d+) (\\d+) \"(.*?)\" \"(.*?)\"",
        "event_type": "web_access",
        "log_category": "application",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "apache",
        "event_id": "apache_error",
        "event_cn": "Apache错误日志",
        "regex": "(?i)apache\\[\\d+\\]: \\[error\\] \\[client (\\S+)\\] (.*?)(File does not exist|Permission denied): (.*?)",
        "event_type": "web_error",
        "log_category": "application",
        "level": 4,
        "level_cn": "中高"
    },
    {
        "program": "apache",
        "event_id": "apache_cgi_exec",
        "event_cn": "Apache CGI脚本执行",
        "regex": "(?i)apache\\[\\d+\\]: (\\S+) - - \\[(.*?)\\] \"(\\S+) (.*?\\.cgi|.*?\\.pl) HTTP/\\d+\\.\\d+\" 200 (\\d+)",
        "event_type": "web_exec",
        "log_category": "application",
        "level": 2,
        "level_cn": "中低"
    },

    # 3. Tomcat 日志规则
    {
        "program": "tomcat",
        "event_id": "tomcat_access",
        "event_cn": "Tomcat访问日志",
        "regex": "(?i)tomcat\\[\\d+\\]: (\\S+) - - \\[(.*?)\\] \"(\\S+) (.*?) HTTP/\\d+\\.\\d+\" (\\d+) (\\d+) (\\d+)",
        "event_type": "web_access",
        "log_category": "application",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "tomcat",
        "event_id": "tomcat_application_error",
        "event_cn": "Tomcat应用异常",
        "regex": "(?i)tomcat\\[\\d+\\]: SEVERE: (.*?)Exception in (servlet|filter) (.*?) for context path (.*?)",
        "event_type": "web_application_error",
        "log_category": "application",
        "level": 5,
        "level_cn": "中高"
    },

    # 4. 通用Web安全场景
    {
        "program": "nginx|apache|tomcat",
        "event_id": "web_unauthorized",
        "event_cn": "Web未授权访问(401)",
        "regex": "(?i)(nginx|apache|tomcat)\\[\\d+\\]: (\\S+) - - \\[(.*?)\\] \"(\\S+) (.*?) HTTP/\\d+\\.\\d+\" 401 (\\d+)",
        "event_type": "web_security",
        "log_category": "application",
        "level": 3,
        "level_cn": "中"
    },
    {
        "program": "nginx|apache",
        "event_id": "web_gateway_error",
        "event_cn": "Web网关错误(502)",
        "regex": "(?i)(nginx|apache)\\[\\d+\\]: (\\S+) - - \\[(.*?)\\] \"(\\S+) (.*?) HTTP/\\d+\\.\\d+\" 502 (\\d+)",
        "event_type": "web_error",
        "log_category": "application",
        "level": 5,
        "level_cn": "中高"
    },
    {
        "program": "nginx|apache",
        "event_id": "web_sensitive_file",
        "event_cn": "Web敏感文件访问",
        "regex": "(?i)(nginx|apache)\\[\\d+\\]: (\\S+) - - \\[(.*?)\\] \"(\\S+) (/robots.txt|/.htaccess|/.git|/config.php) HTTP/\\d+\\.\\d+\" (\\d+)",
        "event_type": "web_security",
        "log_category": "application",
        "level": 3,
        "level_cn": "中"
    },

    # 原有Nginx基础规则（保留并补充）
    {
        "program": "nginx",
        "event_id": "nginx_request_processed",
        "event_cn": "Nginx处理HTTP请求",
        "regex": "(?i)nginx\\[\\d+\\]: (\\S+) - - \"(\\S+) (\\S+) (\\S+)\" (\\d+) (\\d+)",
        "event_type": "web_access",
        "log_category": "application",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "nginx",
        "event_id": "nginx_error_occurred",
        "event_cn": "Nginx发生错误",
        "regex": "(?i)nginx\\[\\d+\\]: \\S+ \\[error\\] (\\d+)#(\\d+): (.*)",
        "event_type": "web_error",
        "log_category": "application",
        "level": 4,
        "level_cn": "中高"
    },
    
    # CRON错误补充
    {
        "program": "CRON",
        "event_id": "cron_job_failed",
        "event_cn": "CRON定时任务失败",
        "regex": "(?i)CRON\\[\\d+\\]: \\((\\S+)\\) ERROR \\((.*)\\)",
        "event_type": "scheduled_task_failure",
        "log_category": "system",
        "level": 5,
        "level_cn": "中高"
    },
    {
        "program": "CRON",
        "event_id": "cron_session_open",
        "event_cn": "CRON会话开启",
        "regex": "(?i)CRON\\[\\d+\\]: pam_unix\\(cron:session\\): session opened for user (\\S+) by \\(uid=\\d+\\)",
        "event_type": "scheduled_task",
        "log_category": "system",
        "level": 1,
        "level_cn": "低"
    },
    {
        "program": "CRON",
        "event_id": "cron_session_closed",
        "event_cn": "CRON会话关闭",
        "regex": "(?i)CRON\\[\\d+\\]: pam_unix\\(cron:session\\): session closed for user (\\S+)",
        "event_type": "scheduled_task",
        "log_category": "system",
        "level": 1,
        "level_cn": "低"
    }
]
