from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls  import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    """注销用户"""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
    """注册新用户"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录，再重定向到主页
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)

"""
我们首先导入了函数render()，然后导入了函数login()和authenticate()，以便在用户正确 地填写了注册信息时让其自动登录。我们还导入了默认表
单UserCreationForm。在函数register() 中，我们检查要响应的是否是POST请求。如果不是，就创建一个UserCreationForm实例，且不给 它提供任
何初始数据。
如果响应的是POST请求，我们就根据提交的数据创建一个UserCreationForm实例(见)，并检查这些数据是否有效:就这里而言，是用户名未包含非法字
符，输入的两个密码相同，以及用户没有试图做恶意的事情。
如果提交的数据有效，我们就调用表单的方法save()，将用户名和密码的散列值保存到数据 库中(见)。方法save()返回新创建的用户对象，我们将其存
储在new_user中。保存用户的信息后，我们让用户自动登录，这包含两个步骤。首先，我们调用authenticate()， 并将实参new_user.username和密码
传递给它(见)。用户注册时，被要求输入密码两次;由于 表单是有效的，我们知道输入的这两个密码是相同的，因此可以使用其中任何一个。在这里，我
们从表单的POST数据中获取与键'password1'相关联的值。如果用户名和密码无误，方法 authenticate()将返回一个通过了身份验证的用户对象，而我们
将其存储在authenticated_user 8 中。接下来，我们调用函数login()，并将对象request和authenticated_user传递给它(见)， 这将为新用户创
建有效的会话。最后，我们将用户重定向到主页(见)，其页眉中显示了一条 个性化的问候语，让用户知道注册成功了
"""

