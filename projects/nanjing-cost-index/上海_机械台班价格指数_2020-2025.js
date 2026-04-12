var zyjxzljListVue = new Vue({
    el: "#queryApp",
    data: {
        titleqc: "汽车式起重机 25t",
        titledt: "双笼施工电梯 ( 中速 ) 安装高度≤ 150m",
        titleqzj: "自升式塔式起重机 2500kN·m",
        Listqc:[],
        RListqc: [ 
                {
                    "name": "2020第四季度",
                    "ch": [
                        { "name": "价格", "value": "43600" },
                        { "name": "指数", "value": "100.00" }
                    ]
                },
                {
                    "name": "2021第一季度",
                    "ch": [
                        { "name": "价格", "value": "43533" },
                        { "name": "指数", "value": "99.85" }
                    ]
                },
                {
                    "name": "2021第二季度",
                    "ch": [
                        { "name": "价格", "value": "43600" },
                        { "name": "指数", "value": "100.00" }
                    ]
                },
                {
                    "name": "2021第三季度",
                    "ch": [
                        { "name": "价格", "value": "43600" },
                        { "name": "指数", "value": "100.00" }
                    ]
                },
                {
                    "name": "2021第四季度",
                    "ch": [
                        { "name": "价格", "value": "43433" },
                        { "name": "指数", "value": "99.62" }
                    ]
                },
                {
                    "name": "2022第一季度",
                    "ch": [
                        { "name": "价格", "value": "43100" },
                        { "name": "指数", "value": "98.85" }
                    ]
                },
                {
                    "name": "2022第二季度",
                    "ch": [
                        { "name": "价格", "value": "43100" },
                        { "name": "指数", "value": "98.85" }
                    ]
                },
                {
                    "name": "2022第三季度",
                    "ch": [
                        { "name": "价格", "value": "43100" },
                        { "name": "指数", "value": "98.85" }
                    ]
                },
                {
                    "name": "2022第四季度",
                    "ch": [
                        { "name": "价格", "value": "43100" },
                        { "name": "指数", "value": "98.85" }
                    ]
                },
                {
                    "name": "2023第一季度",
                    "ch": [
                        { "name": "价格", "value": "43000" },
                        { "name": "指数", "value": "98.62" }
                    ]
                },
                {
                    "name": "2023第二季度",
                    "ch": [
                        { "name": "价格", "value": "41333" },
                        { "name": "指数", "value": "94.80" }
                    ]
                },
                {
                    "name": "2023第三季度",
                    "ch": [
                        { "name": "价格", "value": "40000" },
                        { "name": "指数", "value": "91.74" }
                    ]
                },
                {
                    "name": "2023第四季度",
                    "ch": [
                        { "name": "价格", "value": "40000" },
                        { "name": "指数", "value": "91.74" }
                    ]
                },
                {
                    "name": "2024第一季度",
                    "ch": [
                        { "name": "价格", "value": "40000" },
                        { "name": "指数", "value": "91.74" }
                    ]
                },
                {
                    "name": "2024第二季度",
                    "ch": [
                        { "name": "价格", "value": "40000" },
                        { "name": "指数", "value": "91.74" }
                    ]
                } 
        ],
        Listdt:[],
        RListdt: [ 
                {
                    "name": "2020第四季度",
                    "ch": [
                        { "name": "价格", "value": "26800" },
                        { "name": "指数", "value": "100.00" }
                    ]
                },
                {
                    "name": "2021第一季度",
                    "ch": [
                        { "name": "价格", "value": "26200" },
                        { "name": "指数", "value": "97.76" }
                    ]
                },
                {
                    "name": "2021第二季度",
                    "ch": [
                        { "name": "价格", "value": "26600" },
                        { "name": "指数", "value": "99.25" }
                    ]
                },
                {
                    "name": "2021第三季度",
                    "ch": [
                        { "name": "价格", "value": "26600" },
                        { "name": "指数", "value": "99.25" }
                    ]
                },
                {
                    "name": "2021第四季度",
                    "ch": [
                        { "name": "价格", "value": "26600" },
                        { "name": "指数", "value": "99.25" }
                    ]
                },
                {
                    "name": "2022第一季度",
                    "ch": [
                        { "name": "价格", "value": "26600" },
                        { "name": "指数", "value": "99.25" }
                    ]
                },
                {
                    "name": "2022第二季度",
                    "ch": [
                        { "name": "价格", "value": "26600" },
                        { "name": "指数", "value": "99.25" }
                    ]
                },
                {
                    "name": "2022第三季度",
                    "ch": [
                        { "name": "价格", "value": "26400" },
                        { "name": "指数", "value": "98.51" }
                    ]
                },
                {
                    "name": "2022第四季度",
                    "ch": [
                        { "name": "价格", "value": "26200" },
                        { "name": "指数", "value": "97.76" }
                    ]
                },
                {
                    "name": "2023第一季度",
                    "ch": [
                        { "name": "价格", "value": "26000" },
                        { "name": "指数", "value": "97.01" }
                    ]
                },
                {
                    "name": "2023第二季度",
                    "ch": [
                        { "name": "价格", "value": "25500" },
                        { "name": "指数", "value": "95.15" }
                    ]
                },
                {
                    "name": "2023第三季度",
                    "ch": [
                        { "name": "价格", "value": "24833" },
                        { "name": "指数", "value": "92.66" }
                    ]
                },
                {
                    "name": "2023第四季度",
                    "ch": [
                        { "name": "价格", "value": "24000" },
                        { "name": "指数", "value": "89.55" }
                    ]
                },
                {
                    "name": "2024第一季度",
                    "ch": [
                        { "name": "价格", "value": "24000" },
                        { "name": "指数", "value": "89.55" }
                    ]
                },
                {
                    "name": "2024第二季度",
                    "ch": [
                        { "name": "价格", "value": "23500" },
                        { "name": "指数", "value": "87.69" }
                    ]
                } 
        ],
        Listqzj:[],
        RListqzj: [ 
                {
                    "name": "2020第四季度",
                    "ch": [
                        { "name": "价格", "value": "60800" },
                        { "name": "指数", "value": "100.00" }
                    ]
                },
                {
                    "name": "2021第一季度",
                    "ch": [
                        { "name": "价格", "value": "59433" },
                        { "name": "指数", "value": "97.75" }
                    ]
                },
                {
                    "name": "2021第二季度",
                    "ch": [
                        { "name": "价格", "value": "59600" },
                        { "name": "指数", "value": "98.03" }
                    ]
                },
                {
                    "name": "2021第三季度",
                    "ch": [
                        { "name": "价格", "value": "59000" },
                        { "name": "指数", "value": "97.04" }
                    ]
                },
                {
                    "name": "2021第四季度",
                    "ch": [
                        { "name": "价格", "value": "57333" },
                        { "name": "指数", "value": "94.30" }
                    ]
                },
                {
                    "name": "2022第一季度",
                    "ch": [
                        { "name": "价格", "value": "55833" },
                        { "name": "指数", "value": "91.83" }
                    ]
                },
                {
                    "name": "2022第二季度",
                    "ch": [
                        { "name": "价格", "value": "55800" },
                        { "name": "指数", "value": "91.78" }
                    ]
                },
                {
                    "name": "2022第三季度",
                    "ch": [
                        { "name": "价格", "value": "55467" },
                        { "name": "指数", "value": "91.23" }
                    ]
                },
                {
                    "name": "2022第四季度",
                    "ch": [
                        { "name": "价格", "value": "54600" },
                        { "name": "指数", "value": "89.80" }
                    ]
                },
                {
                    "name": "2023第一季度",
                    "ch": [
                        { "name": "价格", "value": "52333" },
                        { "name": "指数", "value": "86.07" }
                    ]
                },
                {
                    "name": "2023第二季度",
                    "ch": [
                        { "name": "价格", "value": "50333" },
                        { "name": "指数", "value": "82.79" }
                    ]
                },
                {
                    "name": "2023第三季度",
                    "ch": [
                        { "name": "价格", "value": "49000" },
                        { "name": "指数", "value": "80.59" }
                    ]
                },
                {
                    "name": "2023第四季度",
                    "ch": [
                        { "name": "价格", "value": "47333" },
                        { "name": "指数", "value": "77.85" }
                    ]
                },
                {
                    "name": "2024第一季度",
                    "ch": [
                        { "name": "价格", "value": "46900" },
                        { "name": "指数", "value": "77.14" }
                    ]
                },
                {
                    "name": "2024第二季度",
                    "ch": [
                        { "name": "价格", "value": "45067" },
                        { "name": "指数", "value": "74.12" }
                    ]
                } 
        ],
    },
    mounted: function () {
        this.buildData();
        this.loadChatViewqc();
        this.loadChatViewdt();
        this.loadChatViewqzj();
    },
    methods: {
        //数据组合
        buildData: function () {
            var length = 11;
            this.Listqc = [];
            this.Listdt = [];
            this.Listqzj = [];
            for (var i = 0; i < this.RListqc.length; i += length) {
                var arr = this.RListqc.slice(i, i + length);
                this.Listqc.push(arr);
            }
            this.List = [];
            for (var i = 0; i < this.RListdt.length; i += length) {
                var arr = this.RListdt.slice(i, i + length);
                this.Listdt.push(arr);
            }
            this.List = [];
            for (var i = 0; i < this.RListqzj.length; i += length) {
                var arr = this.RListqzj.slice(i, i + length);
                this.Listqzj.push(arr);
            }
        },
        //加载图
        loadChatViewqc: function () {
            var _this = this;
            var data = [];
            var months = [];
            var first = _this.RListqc;

            first.forEach(function (firstitem) {
                months.push(firstitem.name);
                data.push(firstitem.ch[1].value);
            });
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('qc'));
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: _this.titleqc + "指数指标趋势图",
                    x: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'line'
                    }
                },
                legend: {
                    data: [_this.titleqc + '指数指标'],
                    x: 'right'
                },
                dataZoom: [
                    {
                        show: true,
                        realtime: true,
                        xAxisIndex: 0,
                        filterMode: 'filter'
                    }
                ],
                grid: {
                    left: 50,
                    right: 50,
                    bottom: 50,
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: true,
                    data: months
                },
                yAxis: {
                    name: '',
                    type: 'value'
                },
                series: [
                    {
                        name: _this.titleqc + '指数指标',
                        type: 'line',
                        data: data
                    },
                ]
            };
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },
        loadChatViewdt: function () {
            var _this = this;
            var data = [];
            var months = [];
            var first = _this.RListdt;

            first.forEach(function (firstitem) {
                months.push(firstitem.name);
                data.push(firstitem.ch[1].value);
            });
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('dt'));
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: _this.titledt + "指数指标趋势图",
                    x: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'line'
                    }
                },
                legend: {
                    data: [_this.titledt + '指数指标'],
                    x: 'right'
                },
                dataZoom: [
                    {
                        show: true,
                        realtime: true,
                        xAxisIndex: 0,
                        filterMode: 'filter'
                    }
                ],
                grid: {
                    left: 50,
                    right: 50,
                    bottom: 50,
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: true,
                    data: months
                },
                yAxis: {
                    name: '',
                    type: 'value'
                },
                series: [
                    {
                        name: _this.titledt + '指数指标',
                        type: 'line',
                        data: data
                    },
                ]
            };
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },
        loadChatViewqzj: function () {
            var _this = this;
            var data = [];
            var months = [];
            var first = _this.RListqzj;

            first.forEach(function (firstitem) {
                months.push(firstitem.name);
                data.push(firstitem.ch[1].value);
            });
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('qzj'));
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: _this.titleqzj + "指数指标趋势图",
                    x: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'line'
                    }
                },
                legend: {
                    data: [_this.titleqzj + '指数指标'],
                    x: 'right'
                },
                dataZoom: [
                    {
                        show: true,
                        realtime: true,
                        xAxisIndex: 0,
                        filterMode: 'filter'
                    }
                ],
                grid: {
                    left: 50,
                    right: 50,
                    bottom: 50,
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: true,
                    data: months
                },
                yAxis: {
                    name: '',
                    type: 'value'
                },
                series: [
                    {
                        name: _this.titleqzj + '指数指标',
                        type: 'line',
                        data: data
                    },
                ]
            };
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },
    }
});