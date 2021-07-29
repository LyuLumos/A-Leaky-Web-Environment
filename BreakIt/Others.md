# 其他漏洞环境的杂乱总结

由于时间关系以及校内堪忧的访问速度，其他的环境并没有完整的记录下来，这里只是杂乱地总结一下部分小组的漏洞设计。

## SQL注入

sql注入是大家采用最多的漏洞，原理也比较简单，在于查询语句的字符串拼接，解决方法是传入参数而不是字符串拼接。引用知乎上的一句话来说

> 程序员不应该执行删除地球这样的SQL语句，而是写删除一个行星，然后将地球当作参数传入。



## SSTI: flask 模板注入漏洞

核心原理：不正确地使用 `flask` 中的 `render_template_string` 方法会引发 `SSTI`。

漏洞代码示例（其他组代码也没公开只能自己口胡一个）

```py
@app.route('/test/')
def test():
    code = request.args.get('id')
    html = '''
        <h3>%s</h3>
    '''%(code)
    return render_template_string(html)
```

这段代码直接将用户的输入作为代码模板运行，所以肯定无法阻止类似XSS攻击这样的行为。


## XXE: XML外部实体注入攻击

XXE的攻击原理是：通常攻击者会将payload注入XML文件中，一旦文件被执行，将会读取服务器上的本地文件，并对内网发起访问扫描内部网络端口。

下面我们用一个简要的示例说明：

一个简单的XML代码POST请求为：

```html

<!-- 省略不必要的内容 -->

<?xml version="1.0"?>
<catalog>
   <core id="test101">
      <!-- 省略不必要的内容 -->
   </core>
</catalog>
```

添加恶意的payload，则代码变成

```html
<?xml version="1.0"?>
<!DOCTYPE GVI [<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<catalog>...</catalog>
```

服务器就会返回 `/etc/passwd` 文件。有一个组（忘了具体是哪个了...）使用了这个漏洞，利用XXE访问 `d:/password.txt` 即可得到结果。

