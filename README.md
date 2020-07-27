# yyam: include-yy's account manager

## 0x00 目的

当今，个人的网上账户数量不断增长，不知不觉间可能就有了二三十个账号。除了一些常用的账号比如微信，QQ，其他的可能过一段时间后就会忘记，即便可以通过邮箱或电话找回，也得费一番时间和力气。

一种解决方式是使用备忘录记录账号信息。之前我就是直接将账号记录在 txt 文本中，并把文件放在云上，方便随时查找。我使用过的文本格式如下：

```
[username]
[id]&[password]
...
```

对于少量的账号和密码，这样做是十分有效的，但是账号数量太多会导致查找和修改的困难。编辑器的查找功能可以缓解这个问题。若多个账号使用相同的用户名会使得查找范围过大、在同一网站下注册多个账号，若在搜索时指定网站名会得到多个搜索结果。

我编写这个小程序的目的就是解决上面的问题，即：

- 允许同时指定多个搜索选项，比如网站，用户名，id

- 支持单个网站下存储多个账号

## 0x01 文件格式

账号的存储格式有很多种选择，我在查看 rust 文档时偶然发现 cargo 的配置文件使用的是[toml](https://toml.io/en/) 格式，相比于 json，它的可读性要高很多，这样即便无法使用账号管理器也可以较为轻松地查看账户信息。

账号的格式如下：

```
[WebSiteName]
total_number = (number)

[WebSiteName:(order_number)]
id = (user-id-string)
username = (username-string)
password = (password-string)
email = (email-array-string)
phone_number = (phone-number-string)
[serverName:(order):histroy]
used_username = [[history-user-name-string, last-time-used-time-format]...]
used_password = [[history-pwd-string, last-time-format]...]
used_email = [[email-string, time]]
used_phone_number = [[phone-string, time]]
[WebSiteName:(order):info]
modify_time = (time-format)
modify_count = number
[serverName:(order):etc]
...
```

- \[Website] 是网站名

- total\_number 是该网站下的账号个数

- id、username、password、email 和 phone\_number 是账户的常用属性

- history 项是一个记录表，记录账户之前使用过的一些属性的信息

- info 记录账户的修改时间和修改次数

- etc 是账户的其他信息，由用户自定义

网站和 id 唯一确定一个账号。

## 0x02 安装，使用与配置

### 安装

可以使用 pip 直接安装：

```
pip install yyam
```

也可以下载源代码后，在项目根目录执行：

```
python setup.py sdist
```

移动到 dist 目录并执行：

```
pip install yyam-0.1.tar.gz
```

### 配置

在第一次使用之前，首先需要配置存储账户文件的位置，使用 `-c` 或 `--config` 来指定位置，例如，存储文件 `yy.txt` 在 `/home` 目录下，则：

```
yyam -c /home/yy.txt
```

如果变更了文件的位置，再次使用新的目录进行配置即可。

若要删除目录，可以使用 "" 来作为 `-c` 选项的参数

### 使用

运行 `yyam -h` 或 `yyam --help`，可以看到如下帮助信息（大概是这样）

```
usage: yyam [-h] [-a items [items ...] | -m items [items ...] | -d items [items ...] | -s [items [items ...]] | -l |
            -la | -c file-path] [-w website] [-i id] [-u name] [-p password] [-e email] [-n phone] [-f filename]
            [-o filename]

include-yy's account manager

optional arguments:
  -h, --help            show this help message and exit
  -a items [items ...], --add items [items ...]
                        add new item, it can be website(w), username(u), password(p), email(e) and phone-number(n)
                        [wupen]+
  -m items [items ...], --modify items [items ...]
                        modify exist items, it can be username(u), password(p), email(e) and phone-number(n) [upen]+
  -d items [items ...], --delete items [items ...]
                        delete exist items, it can be website(w), id(i), username(u), password(p), email(e) and phone
                        number(n) [wuipen]+
  -s [items [items ...]], --search [items [items ...]]
                        search exist items, it can be website(w), id(i), username(u), password(p) email(e) and phone-
                        number(n). or just no args [wuipen]*
  -l, --list            list website info, include website, id, username
  -la, --list-all       list all website info, include password, email and phone number
  -c file-path, --configure file-path
                        configure the default file path
  -w website, --website website
                        specify website
  -i id, --id id        specify id
  -u name, --username name
                        specify username
  -p password, --password password
                        specify password
  -e email, --email email
                        specify email
  -n phone, --phone-number phone
                        specify phone number
  -f filename, --filename filename
                        specify file to read (optional)
  -o filename, --output-file filename
                        specify output file (optional)

author: include-yy, last modified time: 2020.7.26, 14:07, utc+8
```

如上所述，-h 和 --help 显示帮助信息，其他的选项功能如下所述：

在介绍功能参数前，首先需要介绍查找参数。

#### 查找参数 -w -u -i -p -e -n

wuipen 即账户的各个属性：网站，用户名，id，密码，邮箱和电话。这六个属性可以这样记忆：Windows UI pen :p

指定某个搜索选项后，选项的参数即使搜索的内容，比如 -w qq 就是搜索所有包含 “qq” 字符串的账号，-u include-yy 就是搜索所有用户名包含 "include-yy" 的账号。

注意我的用词 ”包含“ 而不是”是“。搜索使用的字符串并不是用来进行完全匹配的，它们被看作是正则表达式。使用 qq 来搜索可能会得到 qqa，qqb，myqq 等网站的账号，如果想要对某个选项进行精准匹配，那就使用正则的方法吧：`^qq$`

如果指定的各个搜索选项得到的结果交集为空，那么就会得到空的搜索结果。一般而言，指定 -w 和 -i 足以得到想要的账号了。

**尽量不要使用 -p 来进行搜索，虽然我提供了这个选项**

#### 添加 -a

`-a` 选项向文件中添加一个新的账号，或是向已有账号添加新的属性。

-a 接收的参数的正则表示为 `[wupen]+`，即一个或多个字符串，字符串的字符可以是 w u p e n，它们分别代表 website(w)，username(u)，password(p)，email(e) 和 phone\_number(n)。其中，w 选项不能与其他选项共存。

指定选项后，程序会提示你输入相关的信息，若不想输入，可以使用 `:q` ，`:q!` 和 `:!q` 命令推出程序。

#### 修改 -m

`-m` 选项修改某个账号的属性

-m 可以修改账号的 upen 属性，即用户名、密码、邮箱和电话号码

指定选项后，程序会提示你输入新的信息

#### 删除 -d

`-d` 选项可以删除账号或账号中的某一信息

若指定了 w ，则删除某个网站和与之关联的所有账号，若指定了 i ，则删除账号，upen 对应账号中的各个属性

#### 查找 -s

`-d` 选项显示查找到的账号中的指定的信息

它的参数可以是 wuipen，若没有指定参数，默认显示 wui，全部指定则显示账号的全部信息

#### 列出 -l -la

列出所有的账号的信息，-l 只列出 wui，而 -la 会全部列出，包括密码，邮箱和电话号码

在使用 -la 选项时，程序会提示你检查周围是否有人或监控的存在，如果你确定没有，可以输入 `yy` 或 `include-yy` 让其执行下一步操作，即显示所有账号的所有信息，否则程序退出。

#### 指定文件 -f -o

如果你不想使用默认的存储文件，那么你可以使用 -f 来指定输入文件，使用 -o 来指定输出文件。

## 0x03 使用示例

这里使用 qq 来作为示例

首先，添加一个账号：

```
>yyam -w a 
please input website :
qq
please input id :
123456
please input username :
123456
please input password :
123456
please input email :
123456@qq.com
please input phone number :
:q
operation add successfully finishedlly finished
```

完成后查看存储文件：

```
[qq]
total_number = 1

[qq.1]
username = "123456"
password = "123456"
id = "123456"
email = "123456@qq.com"
phone_number = ""

[qq.1.history]
used_username = []
used_password = []
used_email = []
used_phone_number = []

[qq.1.info]
modify_time = 2020-07-27T15:02:51.760751
modify_count = 1

[qq.1.etc]
```

可以看到账户的信息，其中，电话号码输入时使用了 :q，表示不输入电话号码，如果使用了感叹号（:q!, :!q），程序会直接退出，取消添加操作。（其他选项的退出也大抵如此）

下面使用 -a n 选项为它加上电话号码（由于只有一个账号，使用 -w qq 足以查找到对应账号）

```
>yyam -a n -w qq
please input phone number :
123456
operation add successfully finished
```

修改的话，使用 -d。这里假设我要修改密码：

```
>yyam -m p -w qq
please input password :
111111
operation modify successfully finished
```

再添加一个账号：

```
>yyam -a w
please input website :
qq
please input id :
111222
please input username :
111222
please input password :
111222
please input email :
111222@qq.com
please input phone number :
111222
operation add successfully finished
```

现在，存储文件中就有了两个账号，都属于网站 qq。

使用 -s wui 可以查找网站的信息：

```
>yyam -s wui
website     : qq
id          : 123456
username    : 123456
website     : qq
id          : 111222
username    : 111222
operation search successfully finished
```

使用 -d w 或 -d i 可以对这两个账号进行删除操作：

```
>yyam -d i -w qq
1 :
website : qq
id      : 123456
username: 123456
2 :
website : qq
id      : 111222
username: 111222
please input order number :
1
operation delete successfully finished
```

现在再列出账号：

```
>yyam -l
website     : qq
id          : 111222
username    : 111222

operation list successfully finished
```

可以发现只剩下可第二个账号。其他的删除操作大同小异，这里不一一赘述了。

使用 -la 选项需要输入作者（就是我）的名字，以此提示你检查周围是否有人（你也可以在 list\_item.py 中改成你想使用的名字）

```
>yyam -la
make sure there is nobody around you
please input author' name for validation :
yy
website     : qq
id          : 111222
username    : 111222
password    : 111222
email       : 111222@qq.com
phone number: 111222

operation list_all successfully finished
```

## 0x04 安全考虑

这个小程序一定程度上解决了普通文本文件存储密码的一些问题，但是对存储的安全性的改进效果几乎是微乎其微，这里只能给出几点建议：

- 不要在人多的地方使用该程序

- 对已存储的账号进行备份

- 不要让别人动你的计算机

- 若长时间不使用该程序，请及时卸载或删除存储文件路径

本程序未使用任何的网络功能，也没有使用所谓的键盘钩子来监视用户的键盘输入，所以不用担心我来窃取你的账号。你可以阅读源代码来判断是否满足你的安全要求。

## 0x05 其他

如果你看的仔细的话，你会发现还有一个 etc 项没有提，这部分我目前还没有为它提供一个比较好的接口，你可以直接在文件中对它进行增删查改，我会在之后的版本中为对 etc 项目的操作提供支持。

如果在使用过程中发现了任何异常抛出或 bug，欢迎提 issue 和直接向我发邮件。

email: 969041171@qq.com

include-yy 2020.7.27 15.19 utc+8
