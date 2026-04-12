var zycljgListVue = new Vue({
    el: "#queryApp",
    data: {
        titlegj: "综合钢筋", 
        titlehnt: "综合混凝土", 
        titlezzpsgj: "综合预制装配式构件", 
        Listgj:[],
         RListgj: [
                {
                    "name": "2019第一季度",
                    "ch": [
                        { "name": "价格", "value": "3711" },
                        { "name": "指数", "value": "100" }
                    ]
                },
                {
                    "name": "2019第二季度",
                    "ch": [
                        { "name": "价格", "value": "3966" },
                        { "name": "指数", "value": "106.87" }
                    ]
                },
                {
                    "name": "2019第三季度",
                    "ch": [
                        { "name": "价格", "value": "3831" },
                        { "name": "指数", "value": "103.23" }
                    ]
                },
                {
                    "name": "2019第四季度",
                    "ch": [
                        { "name": "价格", "value": "3868" },
                        { "name": "指数", "value": "104.23" }
                    ]
                },
                {
                    "name": "2020第一季度",
                    "ch": [
                        { "name": "价格", "value": "3594" },
                        { "name": "指数", "value": "96.85" }
                    ]
                },
                {
                    "name": "2020第二季度",
                    "ch": [
                        { "name": "价格", "value": "3512" },
                        { "name": "指数", "value": "94.64" }
                    ]
                },
                {
                    "name": "2020第三季度",
                    "ch": [
                        { "name": "价格", "value": "3619" },
                        { "name": "指数", "value": "97.52" }
                    ]
                },
                {
                    "name": "2020第四季度",
                    "ch": [
                        { "name": "价格", "value": "3855" },
                        { "name": "指数", "value": "103.88" }
                    ]
                },
                {
                    "name": "2021第一季度",
                    "ch": [
                        { "name": "价格", "value": "4241" },
                        { "name": "指数", "value": "114.28" }
                    ]
                },
                {
                    "name": "2021第二季度",
                    "ch": [
                        { "name": "价格", "value": "4900" },
                        { "name": "指数", "value": "132.04" }
                    ]
                },
                {
                    "name": "2021第三季度",
                    "ch": [
                        { "name": "价格", "value": "4950" },
                        { "name": "指数", "value": "133.39" }
                    ]
                },
                {
                    "name": "2021第四季度",
                    "ch": [
                        { "name": "价格", "value": "5043" },
                        { "name": "指数", "value": "135.89" }
                    ]
                },
                {
                    "name": "2022第一季度",
                    "ch": [
                        { "name": "价格", "value": "4620" },
                        { "name": "指数", "value": "124.49" }
                    ]
                },
                {
                    "name": "2022第二季度",
                    "ch": [
                        { "name": "价格", "value": "4641" },
                        { "name": "指数", "value": "125.06" }
                    ]
                },
                {
                    "name": "2022第三季度",
                    "ch": [
                        { "name": "价格", "value": "4055" },
                        { "name": "指数", "value": "109.27" }
                    ]
                },
                {
                    "name": "2022第四季度",
                    "ch": [
                        { "name": "价格", "value": "3864" },
                        { "name": "指数", "value": "104.12" }
                    ]
                },
                {
                    "name": "2023第一季度",
                    "ch": [
                        { "name": "价格", "value": "4024" },
                        { "name": "指数", "value": "108.43" }
                    ]
                },
                {
                    "name": "2023第二季度",
                    "ch": [
                        { "name": "价格", "value": "3812" },
                        { "name": "指数", "value": "102.73" }
                    ]
                },
                {
                    "name": "2023第三季度",
                    "ch": [
                        { "name": "价格", "value": "3710" },
                        { "name": "指数", "value": "99.97" }
                    ]
                },
                {
                    "name": "2023第四季度",
                    "ch": [
                        { "name": "价格", "value": "3847" },
                        { "name": "指数", "value": "103.66" }
                    ]
                },
                {
                    "name": "2024第一季度",
                    "ch": [
                        { "name": "价格", "value": "3813" },
                        { "name": "指数", "value": "102.75" }
                    ]
                },
                {
                    "name": "2024第二季度",
                    "ch": [
                        { "name": "价格", "value": "3602" },
                        { "name": "指数", "value": "97.06" }
                    ]
                } 
        ],
        Listhnt:[],
        RListhnt: [ 
                {
                    "name": "2019第一季度",
                    "ch": [
                        { "name": "价格", "value": "591.37" },
                        { "name": "指数", "value": "100" }
                    ]
                },
                {
                    "name": "2019第二季度",
                    "ch": [
                        { "name": "价格", "value": "609.49" },
                        { "name": "指数", "value": "103.06" }
                    ]
                },
                {
                    "name": "2019第三季度",
                    "ch": [
                        { "name": "价格", "value": "604.31" },
                        { "name": "指数", "value": "102.19" }
                    ]
                },
                {
                    "name": "2019第四季度",
                    "ch": [
                        { "name": "价格", "value": "652.86" },
                        { "name": "指数", "value": "110.40" }
                    ]
                },
                {
                    "name": "2020第一季度",
                    "ch": [
                        { "name": "价格", "value": "662.89" },
                        { "name": "指数", "value": "112.09" }
                    ]
                },
                {
                    "name": "2020第二季度",
                    "ch": [
                        { "name": "价格", "value": "641.85" },
                        { "name": "指数", "value": "108.54" }
                    ]
                },
                {
                    "name": "2020第三季度",
                    "ch": [
                        { "name": "价格", "value": "620.82" },
                        { "name": "指数", "value": "104.98" }
                    ]
                },
                {
                    "name": "2020第四季度",
                    "ch": [
                        { "name": "价格", "value": "683.28" },
                        { "name": "指数", "value": "115.54" }
                    ]
                },
                {
                    "name": "2021第一季度",
                    "ch": [
                        { "name": "价格", "value": "688.78" },
                        { "name": "指数", "value": "116.47" }
                    ]
                },
                {
                    "name": "2021第二季度",
                    "ch": [
                        { "name": "价格", "value": "706.41" },
                        { "name": "指数", "value": "119.45" }
                    ]
                },
                {
                    "name": "2021第三季度",
                    "ch": [
                        { "name": "价格", "value": "683.39" },
                        { "name": "指数", "value": "115.56" }
                    ]
                },
                {
                    "name": "2021第四季度",
                    "ch": [
                        { "name": "价格", "value": "751.67" },
                        { "name": "指数", "value": "127.11" }
                    ]
                },
                {
                    "name": "2022第一季度",
                    "ch": [
                        { "name": "价格", "value": "693.42" },
                        { "name": "指数", "value": "117.26" }
                    ]
                },
                {
                    "name": "2022第二季度",
                    "ch": [
                        { "name": "价格", "value": "671.74" },
                        { "name": "指数", "value": "113.59" }
                    ]
                },
                {
                    "name": "2022第三季度",
                    "ch": [
                        { "name": "价格", "value": "637.43" },
                        { "name": "指数", "value": "107.79" }
                    ]
                },
                {
                    "name": "2022第四季度",
                    "ch": [
                        { "name": "价格", "value": "668.82" },
                        { "name": "指数", "value": "113.10" }
                    ]
                },
                {
                    "name": "2023第一季度",
                    "ch": [
                        { "name": "价格", "value": "663.65" },
                        { "name": "指数", "value": "112.22" }
                    ]
                },
                {
                    "name": "2023第二季度",
                    "ch": [
                        { "name": "价格", "value": "653.61" },
                        { "name": "指数", "value": "110.52" }
                    ]
                },
                {
                    "name": "2023第三季度",
                    "ch": [
                        { "name": "价格", "value": "621.90" },
                        { "name": "指数", "value": "105.16" }
                    ]
                },
                {
                    "name": "2023第四季度",
                    "ch": [
                        { "name": "价格", "value": "628.05" },
                        { "name": "指数", "value": "106.20" }
                    ]
                },
                {
                    "name": "2024第一季度",
                    "ch": [
                        { "name": "价格", "value": "629.02" },
                        { "name": "指数", "value": "106.37" }
                    ]
                },
                {
                    "name": "2024第二季度",
                    "ch": [
                        { "name": "价格", "value": "618.34" },
                        { "name": "指数", "value": "104.56" }
                    ]
                } 
        ],
        Listyzzpsgj:[],
        RListyzzpsgj: [ 
                {
                    "name": "2019第一季度",
                    "ch": [
                        { "name": "价格", "value": "3305" },
                        { "name": "指数", "value": "100" }
                    ]
                },
                {
                    "name": "2019第二季度",
                    "ch": [
                        { "name": "价格", "value": "3298" },
                        { "name": "指数", "value": "99.79" }
                    ]
                },
                {
                    "name": "2019第三季度",
                    "ch": [
                        { "name": "价格", "value": "3277" },
                        { "name": "指数", "value": "99.15" }
                    ]
                },
                {
                    "name": "2019第四季度",
                    "ch": [
                        { "name": "价格", "value": "3259" },
                        { "name": "指数", "value": "98.61" }
                    ]
                },
                {
                    "name": "2020第一季度",
                    "ch": [
                        { "name": "价格", "value": "3244" },
                        { "name": "指数", "value": "98.15" }
                    ]
                },
                {
                    "name": "2020第二季度",
                    "ch": [
                        { "name": "价格", "value": "3153" },
                        { "name": "指数", "value": "95.40" }
                    ]
                },
                {
                    "name": "2020第三季度",
                    "ch": [
                        { "name": "价格", "value": "3063" },
                        { "name": "指数", "value": "92.68" }
                    ]
                },
                {
                    "name": "2020第四季度",
                    "ch": [
                        { "name": "价格", "value": "3143" },
                        { "name": "指数", "value": "95.10" }
                    ]
                },
                {
                    "name": "2021第一季度",
                    "ch": [
                        { "name": "价格", "value": "3161" },
                        { "name": "指数", "value": "95.64" }
                    ]
                },
                {
                    "name": "2021第二季度",
                    "ch": [
                        { "name": "价格", "value": "3235" },
                        { "name": "指数", "value": "97.89" }
                    ]
                },
                {
                    "name": "2021第三季度",
                    "ch": [
                        { "name": "价格", "value": "3176" },
                        { "name": "指数", "value": "96.10" }
                    ]
                },
                {
                    "name": "2021第四季度",
                    "ch": [
                        { "name": "价格", "value": "3327" },
                        { "name": "指数", "value": "100.67" }
                    ]
                },
                {
                    "name": "2022第一季度",
                    "ch": [
                        { "name": "价格", "value": "3257" },
                        { "name": "指数", "value": "98.55" }
                    ]
                },
                {
                    "name": "2022第二季度",
                    "ch": [
                        { "name": "价格", "value": "3262" },
                        { "name": "指数", "value": "98.70" }
                    ]
                },
                {
                    "name": "2022第三季度",
                    "ch": [
                        { "name": "价格", "value": "3210" },
                        { "name": "指数", "value": "97.13" }
                    ]
                },
                {
                    "name": "2022第四季度",
                    "ch": [
                        { "name": "价格", "value": "3205" },
                        { "name": "指数", "value": "96.97" }
                    ]
                },
                {
                    "name": "2023第一季度",
                    "ch": [
                        { "name": "价格", "value": "3218" },
                        { "name": "指数", "value": "97.37" }
                    ]
                },
                {
                    "name": "2023第二季度",
                    "ch": [
                        { "name": "价格", "value": "3195" },
                        { "name": "指数", "value": "96.67" }
                    ]
                },
                {
                    "name": "2023第三季度",
                    "ch": [
                        { "name": "价格", "value": "3154" },
                        { "name": "指数", "value": "95.43" }
                    ]
                },
                {
                    "name": "2023第四季度",
                    "ch": [
                        { "name": "价格", "value": "3178" },
                        { "name": "指数", "value": "96.16" }
                    ]
                },
                {
                    "name": "2024第一季度",
                    "ch": [
                        { "name": "价格", "value": "3147" },
                        { "name": "指数", "value": "95.22" }
                    ]
                },
                {
                    "name": "2024第二季度",
                    "ch": [
                        { "name": "价格", "value": "3133" },
                        { "name": "指数", "value": "94.80" }
                    ]
                } 
        ],  
    },
    mounted: function () {
        this.buildData();
        this.loadChatViewgj();
        this.loadChatViewhnt();
        this.loadChatViewzzpsgj();
    },
    methods: {
        //数据组合
        buildData: function () {
            var length = 11;
            this.Listgj = [];
            this.Listhnt = [];
            this.Listyzzpsgj = [];
            for (var i = 0; i < this.RListgj.length; i += length) {
                var arr = this.RListgj.slice(i, i + length);
                this.Listgj.push(arr);
            }
            this.List = [];
            for (var i = 0; i < this.RListhnt.length; i += length) {
                var arr = this.RListhnt.slice(i, i + length);
                this.Listhnt.push(arr);
            }
            this.List = [];
            for (var i = 0; i < this.RListyzzpsgj.length; i += length) {
                var arr = this.RListyzzpsgj.slice(i, i + length);
                this.Listyzzpsgj.push(arr);
            }
        },
        //加载图
        loadChatViewgj: function () {
            var _this = this;
            var data = [];
            var months = [];
            var first = _this.RListgj;

            first.forEach(function (firstitem) {
                months.push(firstitem.name);
                data.push(firstitem.ch[1].value);
            }); 
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('gj'));
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: _this.titlegj + "指数指标趋势图",
                    x: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'line'
                    }
                },
                legend: {
                    data: [_this.titlegj + '指数指标'],
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
                        name: _this.titlegj + '指数指标',
                        type: 'line',
                        data: data
                    },
                ]
            }; 
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },
        loadChatViewhnt: function () {
            var _this = this;
            var data = [];
            var months = [];
            var first = _this.RListhnt;

            first.forEach(function (firstitem) {
                months.push(firstitem.name);
                data.push(firstitem.ch[1].value);
            });
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('hnt'));
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: _this.titlehnt + "指数指标趋势图",
                    x: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'line'
                    }
                },
                legend: {
                    data: [_this.titlehnt + '指数指标'],
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
                        name: _this.titlehnt + '指数指标',
                        type: 'line',
                        data: data
                    },
                ]
            };
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },
        loadChatViewzzpsgj: function () {
            var _this = this;
            var data = [];
            var months = [];
            var first = _this.RListyzzpsgj; 

            first.forEach(function (firstitem) {
                months.push(firstitem.name);
                data.push(firstitem.ch[1].value);
            });
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('zzpsgj'));
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: _this.titlezzpsgj + "指数指标趋势图",
                    x: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'line'
                    }
                },
                legend: {
                    data: [_this.titlezzpsgj + '指数指标'],
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
                        name: _this.titlezzpsgj + '指数指标',
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