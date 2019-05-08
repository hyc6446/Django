/*
 * @Author:
 * @Author:
 * @Date:
 * @lastModify
 * +----------------------------------------------------------------------
 * | WeAdmin 表格table中多个删除等操作公用js
 * | 有改用时直接复制到对应页面也不影响使用
 * +----------------------------------------------------------------------
 */
layui.extend({
	admin: '{/}/static/back/js/admin'
});
layui.use(['form', 'jquery','element'], function() {
	var form = layui.form,
		$ = layui.jquery,
        element = layui.element;

      //自定义验证规则
      form.verify({
          username: function(value){ //value：表单的值、

            if(!new RegExp("^[a-zA-Z][a-zA-Z0-9_]{4,15}$").test(value)){
              return '用户名须已字母开头，允许5-16位字符，允许字母数字下划线';
            }
            //验证账号是否已有
            message=''
            $.ajax({
                async: false,
                data: {
                    username: $('#username').val()
                },
                dataType: 'json',
                success: function(result) {
                    if (result.rel==1) {
                       message += '用户名已存在,请更换一个！'
                    }
                },
                error:function(){
                    message += '数据不正确或未知错误'
                },
                url: $('#path').val() // 这里写你要验证的地址哦。
            });

            if(message!=''){
                return message;
            }
          }
        ,password: [/(.+){6,12}$/, '密码必须6到12位']
        ,repassword: function(value, item){ //value：表单的值、item：表单的DOM对象
            vpwd = $(item).parents('form').find('input[name=password]').val()
            if(value != vpwd ){
              return '两次密码输入不一致！';
            }
          }

      });

    //失去焦点检测用户名是否存在
    $('#username').on('blur', function () {
        //验证账号是否已有
        $.ajax({
            async: false,
            data: {
                username: $('#username').val()
            },
            dataType: 'json',
            success: function(result) {
                //console.log(result)
                if (result.rel==1) {
                    layer.msg('用户名已存在,请更换一个！', {time: 2000, icon:5,offset: '20px',anim: 6});
                }
                if (result.rel==-1) {
                   layer.msg('数据不正确或未知错误', {time: 2000, icon:2,offset: '20px',anim: 6});
                }
            },
            error:function(){
               layer.msg('数据不正确或未知错误', {time: 2000, icon:2,offset: '20px',anim: 6});
            },
            url: $('#path').val() // 这里写你要验证的地址哦。
        });
    });


    //监听提交
      form.on('submit(demo2)',function(data){
        val = $(data.elem).parents('form').find('input[name=agree]').is(':checked')
        if(!val){
            layer.msg('请选择服务条款', {time: 2000, icon:5});
            return false;
        }

      });
});
