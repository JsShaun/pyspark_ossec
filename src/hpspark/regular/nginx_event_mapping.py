def get_event_mapping():
    """Nginx日志事件映射关系（含正则匹配）"""
    return [
        # 1. Nginx访问日志 - 成功请求
        {
            "event_id": "NGX-1001",
            "event_cn": "Nginx处理动态请求成功",
            "event_type": "Web访问",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Information",
            "level_cn": "信息",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \"(POST|PUT|DELETE|PATCH) .+? HTTP/\\d+\\.\\d+\" 200 \\d+"
        },
        {
            "event_id": "NGX-1002",
            "event_cn": "Nginx处理静态资源成功",
            "event_type": "Web访问",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Information",
            "level_cn": "信息",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \"GET .+?\\.(js|css|jpg|png|gif|ico|svg|html) HTTP/\\d+\\.\\d+\" 200 \\d+"
        },
        {
            "event_id": "NGX-1003",
            "event_cn": "Nginx反向代理请求成功",
            "event_type": "Web访问",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Information",
            "level_cn": "信息",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \"(GET|POST) .+? HTTP/\\d+\\.\\d+\" 200 \\d+ \"-\" \"(.*?)\" \"(\\S+)\""
        },

        # 2. Nginx访问日志 - 重定向与部分成功
        {
            "event_id": "NGX-1010",
            "event_cn": "Nginx请求重定向",
            "event_type": "Web访问",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Information",
            "level_cn": "信息",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \".+?\" (301|302) \\d+"
        },
        {
            "event_id": "NGX-1011",
            "event_cn": "Nginx部分内容请求成功",
            "event_type": "Web访问",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Information",
            "level_cn": "信息",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \".+?\" 206 \\d+"
        },

        # 3. Nginx错误日志 - 客户端错误
        {
            "event_id": "NGX-2001",
            "event_cn": "Nginx请求资源不存在(404)",
            "event_type": "Web错误",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Erro",
            "level_cn": "错误",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \".+?\" 404 \\d+"
        },
        {
            "event_id": "NGX-2002",
            "event_cn": "Nginx权限拒绝(403)",
            "event_type": "Web错误",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Warning",
            "level_cn": "警告",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \".+?\" 403 \\d+"
        },
        {
            "event_id": "NGX-2003",
            "event_cn": "Nginx请求方法不允许(405)",
            "event_type": "Web错误",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Warning",
            "level_cn": "警告",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \".+?\" 405 \\d+"
        },
        {
            "event_id": "NGX-2004",
            "event_cn": "Nginx请求实体过大(413)",
            "event_type": "Web错误",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Warning",
            "level_cn": "警告",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \".+?\" 413 \\d+"
        },

        # 4. Nginx错误日志 - 服务器错误
        {
            "event_id": "NGX-2010",
            "event_cn": "Nginx服务器内部错误(500)",
            "event_type": "Web错误",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Erro",
            "level_cn": "错误",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \".+?\" 500 \\d+"
        },
        {
            "event_id": "NGX-2011",
            "event_cn": "Nginx网关错误(502)",
            "event_type": "Web错误",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Erro",
            "level_cn": "错误",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \".+?\" 502 \\d+"
        },
        {
            "event_id": "NGX-2012",
            "event_cn": "Nginx服务暂时不可用(503)",
            "event_type": "Web错误",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Erro",
            "level_cn": "错误",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \".+?\" 503 \\d+"
        },
        {
            "event_id": "NGX-2013",
            "event_cn": "Nginx网关超时(504)",
            "event_type": "Web错误",
            "log_category": "Application/Web",
            "log_source": "Nginx",
            "level": "Warning",
            "level_cn": "警告",
            "event_regex": "(?i)nginx\[\\d+\]: (\\S+) - - \\[.*?\\] \".+?\" 504 \\d+"
        },

        # 5. Nginx安全事件
        {
            "event_id": "NGX-3001",
            "event_cn": "Nginx检测到SQL注入尝试",
            "event_type": "Web安全",
            "log_category": "Security/Web",
            "log_source": "Nginx",
            "level": "Warning",
            "level_cn": "警告",
            "event_regex": "(?i)nginx\\[\\d+\\]: \\S+ - - \\[.*?\\] \".+?((UNION\\s+SELECT|SELECT\\s+.*?FROM|information_schema|sys\\.schema_units)|(INSERT\\s+INTO|UPDATE\\s+SET|DELETE\\s+FROM|DROP\\s+(TABLE|DATABASE)|TRUNCATE\\s+TABLE)|(OR\\s+1=1|AND\\s+1=1|'\\s+OR\\s+''='|1\\s+OR\\s+'1'='1)|(--|#)|(CONCAT\\(|FLOOR\\(RAND\\(0\\)\\*2\\)|extractvalue\\(|updatexml\\(|version\\(\\))).+?\""
        },
        {
            "event_id": "NGX-3002",
            "event_cn": "Nginx检测到XSS攻击尝试",
            "event_type": "Web安全",
            "log_category": "Security/Web",
            "log_source": "Nginx",
            "level": "Warning",
            "level_cn": "警告",
            # 核心正则：覆盖90%以上常见XSS攻击特征，适配Nginx日志格式
            "event_regex": "(?i)nginx\\[\\d+\\]: \\S+ - - \\[.*?\\] \".+?((<script|</script>|\\x3Cscript|\\%3Cscript)|(on\\w+=|\\son\\w+=)|(javascript:|\\%6Aavascript:|\\x6Aavascript:)|(alert\\(|confirm\\(|prompt\\()|(\\<iframe|\\<img\\s+src=.*?onerror|\\<svg\\s+onload)).+?\""
        },
        {
            "event_id": "NGX-3003",
            "event_cn": "Nginx检测到敏感路径访问",
            "event_type": "Web安全",
            "log_category": "Security/Web",
            "log_source": "Nginx",
            "level": "Warning",
            "level_cn": "警告",
            "event_regex": "(?i)nginx\\[\\d+\\]: \\S+ - - \\[.*?\\] \"(GET|POST|PUT|DELETE|PATCH) \\/(admin|manage|backend|api\\/v\\d+\\/admin|config|backup|sql|system|root|superuser)\\b.*?\""
        },
        {
            "event_id": "NGX-3004",
            "event_cn": "Nginx检测到敏感文件访问尝试",
            "event_type": "Web安全",
            "log_category": "Security/Web",
            "log_source": "Nginx",
            "level": "Warning",
            "level_cn": "警告",
            "event_regex": "(?i)nginx\\[\\d+\\]: \\S+ - - \\[.*?\\] \".+?((\\.env|\\.git|\\.htaccess|\\.user.ini)|(config\\.php|database\\.php|settings\\.php)|(/etc/passwd|/etc/shadow|/proc/self/environ)|(\\.bash_history|\\.ssh/id_rsa)).+?\""
        },


        # 6. Nginx服务管理事件
        {
            "event_id": "NGX-4001",
            "event_cn": "Nginx服务启动成功",
            "event_type": "Web服务管理",
            "log_category": "System/Web",
            "log_source": "Nginx",
            "level": "Information",
            "level_cn": "信息",
            "event_regex": "(?i)nginx\[\\d+\]: nginx: configuration file /etc/nginx/nginx.conf syntax is ok|systemd\[1\]: Started A high performance web server and a reverse proxy server."
        },
        {
            "event_id": "NGX-4002",
            "event_cn": "Nginx服务停止",
            "event_type": "Web服务管理",
            "log_category": "System/Web",
            "log_source": "Nginx",
            "level": "Information",
            "level_cn": "信息",
            "event_regex": "(?i)systemd\[1\]: Stopped A high performance web server and a reverse proxy server.|nginx\[\\d+\]: exiting"
        },
        {
            "event_id": "NGX-4003",
            "event_cn": "Nginx配置重载成功",
            "event_type": "Web服务管理",
            "log_category": "System/Web",
            "log_source": "Nginx",
            "level": "Information",
            "level_cn": "信息",
            "event_regex": "(?i)systemd\[1\]: Reloaded A high performance web server and a reverse proxy server.|nginx\[\\d+\]: configuration file /etc/nginx/nginx.conf test is successful"
        },
        {
            "event_id": "NGX-4004",
            "event_cn": "Nginx配置错误",
            "event_type": "Web服务管理",
            "log_category": "System/Web",
            "log_source": "Nginx",
            "level": "Erro",
            "level_cn": "错误",
            "event_regex": "(?i)nginx\[\\d+\]: nginx: \[emerg\] .+? in /etc/nginx/|nginx\[\\d+\]: configuration file /etc/nginx/nginx.conf test failed"
        }
    ]
