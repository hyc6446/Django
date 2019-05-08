/*
 * @Author:
 * @Author:
 * @Date:
 * @lastModify 2018-3-28
 * +----------------------------------------------------------------------
 * | WeAdmin 表格table中多个删除等操作公用js
 * | 有改用时直接复制到对应页面也不影响使用
 * +----------------------------------------------------------------------
 */
layui.extend({
	admin: '{/}/static/back/js/admin'
});
layui.use(['laydate', 'jquery', 'admin','table','laypage'], function() {
	var laydate = layui.laydate,
		$ = layui.jquery,
		table = layui.table,
		admin = layui.admin,
        laypage = layui.laypage;
     //日期范围
    laydate.render({
        elem: '#date'
        ,range: true
    });

	/*用户-停用*/
	window.member_stop = function (obj, id,url) {
		layer.confirm('确认要修改会员审核状态吗？', function(index) {
			if($(obj).attr('title') == '未审核') {
                statuscode = '已审核'
			} else {
			    statuscode = '未审核'
			}
			//发异步把用户状态进行更改
            $.get(url,{uid:id,stacode:statuscode},function(data){
                location.replace(location.href);

            })

		});
	}
});