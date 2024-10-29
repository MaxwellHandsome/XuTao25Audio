var OriginTitile = document.title,
            titleTime;
        document.addEventListener("visibilitychange", function () {
            if (document.hidden) {
                $('[rel="icon"]').attr("href", "img/my/ban.png");
                document.title = "页面已崩溃！点击恢复！";
                clearTimeout(titleTime);
            } else {
                $('[rel="icon"]').attr("href", "img/my/avatar.png");
                document.title = "(/≧▽≦/)咦！又好了！ " + OriginTitile;
                titleTime = setTimeout(function () {
                    document.title = OriginTitile;
                }, 2000);
            }
        });