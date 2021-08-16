from odoo import models, fields, api


class EpidemicRecord(models.Model):
    _name = 'epidemic.record'

    def default_create_user(self):
        """定义获取当前登录者的函数"""
        return self.env.uid

    name = fields.Char(string='姓名')
    date = fields.Date(string='确诊日期')
    state = fields.Char(string='省')
    city = fields.Char(string='市')
    county = fields.Char(string='区/县')
    street = fields.Char(string='具体地址')
    ill_type = fields.Char(string='感染方式')
    within_or_abroad = fields.Selection([('within', '境内'), ('abroad', '境外')], default='within', string='境内/境外感染')
    is_ill = fields.Boolean(string='是否确诊', default=False)
    begin_lsolation_date = fields.Date(string='起始隔离日期')
    lsolation_mode = fields.Selection([('home', '居家隔离'), ('focus', '集中隔离')], string='隔离方式')
    creat_user_id = fields.Many2one('res.users', string='填报人', default=lambda self: self.env.uid)
    # [lambda self: self.env.uid]拿到当前登录人的id，也可以换一种方式例如函数字段属性中调用default=default_create_user
    note = fields.Text(string='说明')
    test_float = fields.Float(string='测试浮点字段')
    test_int = fields.Integer(string='测试整型字段')

    # 利用Many2many关联字段，初始化一个映射表“epidemic_record_res_users_rel”如果这个参数不填的话，系统也会默认产生一个表名column1··分别为指定产生的字段
    fuzhu_create_user_ids = fields.Many2many('res.users', 'epidemic_record_res_users_rel', column1='record_id',
                                             column2='user_id', string='辅助填报人')
    # active是odoo中预留的字段，当该布尔类型额字段在模型模型中设定为True时，那么模型视图选择数据出现的动作按钮中将会多一个归档的可选值，如
    # 选择归档那么视图中改条数据将不可见，且不可删除
    active = fields.Boolean(default=True)

    @api.model
    def create(self, vals_list):
        """创建记录的时候只执行create方法，不执行write方法。且create方法只执行一次，这里是由于对res.note进行了更改所以又执行write方法"""
        res = super(EpidemicRecord, self).create(vals_list)
        res.note = '{}省{}市，隔离人员姓名{}'.format(res.state, res.city, res.name)
        return res

    def write(self, vals):
        res = super(EpidemicRecord, self).write(vals)
        return res

    @api.onchange('state', 'city', 'name')
    def onchange_note(self):
        """监听省、市、名字"""
        self.note = '{}省{}市，隔离人员姓名'.format(self.state, self.city, self.name)

    # def unlink(self):
    #     """从数据库中删除所选数据集"""
    #     res = super(EpidemicRecord, self).unlink()
    #     return res

    def unlink(self):
        """伪删除"""
        for obj in self:
            obj.active = False
        # 如果进行了伪删除，那么可以在视图对应的action动作中添加如下字段进行过滤出来
        # <field name="context">{'active_test':False}</field>

    def unlink_btn(self):
        for obj in self:
            obj.active = False

    def unlink_cancel_btn(self):
        for obj in self:
            obj.active = True

    def search_test(self):
        """搜索：1.search()；2.browse()"""
        domain = ['|', '|', ('id', '=', 2), ('id', '=', 6), ('id', '=', 7)]
        # 扩展domain表达式，这里是意思为条件('id', '=', 2) | ('id', '=', 6) | ('id', '=', 7)
        # 当然也可以写为domain = [('id', '=', [2,6,7])]或者是[('id', '=', (2,6,7))]
        user_objs1 = self.env['res.users'].search(domain)
        user_objs2 = self.env['res.users'].sudo().browse([2, 6, 7])  # sudo()方法表示跳过res.user中的权限，从而进行browse查询操作
        print('search方法搜索：', user_objs1)  # 在下面的控制台中可以看到输出
        print('browse方法搜索：', user_objs2)

    def create_to_users(self):
        """create的参数用法"""
        res = self.env['res.users'].create({
            'name': '测试账号1',
            'email': '1593574682@163.com',
            'login': 'test1',
        })

    def update_to_users(self):
        """write的参数用法"""
        user_env = self.env['res.users']
        user_id = user_env.search([('name', '=', '测试账号1')])
        # 记录集在调用的write方法的时候，只能是一条记录，如果记录集合中包含多条集合时则需要遍历
        res = user_id.write({
            'login': '1593574682@163.com.cn'
        })
