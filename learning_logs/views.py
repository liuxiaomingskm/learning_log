from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    """The home page for Learning Log"""
    return render(request, 'Learning_logs/index.html')


@login_required
def topics(request):
    """显示所有的主题"""
    # 用户登录后，request对象将有一个user属性，这个属性存储了有关该用户的信息，下
    # 一行代码让django只从数据库中获取owner属性为当前用户的topic对象
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)


    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by(('-date_added'))
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据： 创建一个新表单
        form = TopicForm()

    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


"""
我们导入了HttpResponseRedirect类，用户提交主题后我们将使用这个类将用户重定向到网 页topics。函数reverse()根据指定的URL模型确定URL，
这意味着Django将在页面被请求时生成 URL。我们还导入了刚才创建的表单TopicForm。
4. GET请求和POST请求
创建Web应用程序时，将用到的两种主要请求类型是GET请求和POST请求。对于只是从服务 器读取数据的页面，使用GET请求;在用户需要通过表单提交信息
时，通常使用POST请求。处理 所有表单时，我们都将指定使用POST方法。还有一些其他类型的请求，但这个项目没有使用。
函数new_topic()将请求对象作为参数。用户初次请求该网页时，其浏览器将发送GET请求; 用户填写并提交表单时，其浏览器将发送POST请求。根据请求
的类型，我们可以确定用户请求 的是空表单(GET请求)还是要求对填写好的表单进行处理(POST请求)。
处的测试确定请求方法是GET还是POST。如果请求方法不是POST，请求就可能是GET， 因此我们需要返回一个空表单(即便请求是其他类型的，返回一个
空表单也不会有任何问题)。 我们创建一个TopicForm实例(见)，将其存储在变量form中，再通过上下文字典将这个表单发 送给模板(见)。由于实例
化TopicForm时我们没有指定任何实参，Django将创建一个可供用户 填写的空表单。
如果请求方法为POST，将执行else代码块，对提交的表单数据进行处理。我们使用用户输 入的数据(它们存储在request.POST中)创建一个TopicForm实
例(见)，这样对象form将包含 用户提交的信息。
要将提交的信息保存到数据库，必须先通过检查确定它们是有效的(见)。函数is_valid() 核实用户填写了所有必不可少的字段(表单字段默认都是必不
可少的)，且输入的数据与要求的 字段类型一致(例如，字段text少于200个字符，这是我们在第18章中的models.py中指定的)。这 种自动验证避免了我
们去做大量的工作。如果所有字段都有效，我们就可调用save()(见)， 将表单中的数据写入数据库。保存数据后，就可离开这个页面了。我们使用
reverse()获取页面 topics的URL，并将其传递给HttpResponseRedirect()(见)，后者将用户的浏览器重定向到页 面topics。在页面topics中，
用户将在主题列表中看到他刚输入的主题。
"""


@login_required
def new_entry(request, topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据，创建一个空表格
        form = EntryForm()
    else:
        # POST提交的数据， 对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # commit=false 让Django创建一个新的条目对象，并存储到new_entry中，但不保存到数据库中
            # new_entry.save()保存到数据库中
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据， 对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs: topic',
                                                args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
