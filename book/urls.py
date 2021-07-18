from django.urls import path
# from. import views  # 导入该子应用下的view视图
from book import views

urlpatterns = [
    path('article_new/', views.article_new, name='article_new'),
    path('test_01/<int:xx>', views.test_01, name='test_01'),
    path('inheritage/', views.heritage, name='heritage'),
    path('common/', views.common, name='common'),
    path('showtage/', views.show_tag, name='showtage'),
    path('index_01/', views.index_01, name='index_01'),
    path('add_user/', views.add_user, name='add_user'),  # 测试数据库操作中的的增加
    path('search_user/', views.search_user, name='search_user'),  # 测试数据库操作中的查询
    path('delete_user/', views.delete_user, name='delete_user'),  # 删除数据库中的值
    path('update_user/', views.update_user, name='update_user'),  # 更新数据库中的值
    path('modified_user/', views.modified_user, name='modified_user'),  # 第二种更新数据库中的值
    path('ModifiedWholeFiled/', views.ModifiedWholeFiled, name='ModifiedWholeFiled'),  # 第二种更新数据库中的值
    path('add_book/', views.add_book, name='add_book'),  # 向BookInfo表添加书名，直接以类而非方法/属性的方式
    path('search_book/', views.search_book, name='search_book'),  # 向BookInfo表查询数据，按照id查询
]
