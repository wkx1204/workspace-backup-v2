var zhrgjgListVue = new Vue({
    el: "#queryApp",
    data: {
        title: "综合人工价格",
        List:[],
        RgList: [
                    {
                        "name": "2019第一季度",
                        "ch": [
                            { "name": "价格", "value": "292.57" },
                            { "name": "指数", "value": "100" }
                        ]
                    },
                    {
                        "name": "2019第二季度",
                        "ch": [
                            { "name": "价格", "value": "301.28" },
                            { "name": "指数", "value": "102.98" }
                        ]
                    },
                    {
                        "name": "2019第三季度",
                        "ch": [
                            { "name": "价格", "value": "301.56" },
                            { "name": "指数", "value": "103.07" }
                        ]
                    },
                    {
                        "name": "2019第四季度",
                        "ch": [
                            { "name": "价格", "value": "301.26" },
                            { "name": "指数", "value": "102.97" }
                        ]
                    },
                    {
                        "name": "2020第一季度",
                        "ch": [
                            { "name": "价格", "value": "318.23" },
                            { "name": "指数", "value": "108.77" }
                        ]
                    },
                    {
                        "name": "2020第二季度",
                        "ch": [
                            { "name": "价格", "value": "325.99" },
                            { "name": "指数", "value": "111.42" }
                        ]
                    },
                    {
                        "name": "2020第三季度",
                        "ch": [
                            { "name": "价格", "value": "325.45" },
                            { "name": "指数", "value": "111.24" }
                        ]
                    },
                    {
                        "name": "2020第四季度",
                        "ch": [
                            { "name": "价格", "value": "327.61" },
                            { "name": "指数", "value": "111.98" }
                        ]
                    },
                    {
                        "name": "2021第一季度",
                        "ch": [
                            { "name": "价格", "value": "329.7" },
                            { "name": "指数", "value": "112.69" }
                        ]
                    },
                    {
                        "name": "2021第二季度",
                        "ch": [
                            { "name": "价格", "value": "333.1" },
                            { "name": "指数", "value": "113.85" }
                        ]
                    },
                    {
                        "name": "2021第三季度",
                        "ch": [
                            { "name": "价格", "value": "340.36" },
                            { "name": "指数", "value": "116.33" }
                        ]
                    },
                    {
                        "name": "2021第四季度",
                        "ch": [
                            { "name": "价格", "value": "346.87" },
                            { "name": "指数", "value": "118.56" }
                        ]
                    },
                    {
                        "name": "2022第一季度",
                        "ch": [
                            { "name": "价格", "value": "351.74" },
                            { "name": "指数", "value": "120.22" }
                        ]
                    },
                    {
                        "name": "2022第二季度",
                        "ch": [
                            { "name": "价格", "value": "361.98" },
                            { "name": "指数", "value": "123.72" }
                        ]
                    },
                    {
                        "name": "2022第三季度",
                        "ch": [
                            { "name": "价格", "value": "372.14" },
                            { "name": "指数", "value": "127.2" }
                        ]
                    },
                    {
                        "name": "2022第四季度",
                        "ch": [
                            { "name": "价格", "value": "379.28" },
                            { "name": "指数", "value": "129.64" }
                        ]
                    },
                    {
                        "name": "2023第一季度",
                        "ch": [
                            { "name": "价格", "value": "384.94" },
                            { "name": "指数", "value": "131.57" }
                        ]
                    },
                    {
                        "name": "2023第二季度",
                        "ch": [
                            { "name": "价格", "value": "386.39" },
                            { "name": "指数", "value": "132.07" }
                        ]
                    },
                    {
                        "name": "2023第三季度",
                        "ch": [
                            { "name": "价格", "value": "386.39" },
                            { "name": "指数", "value": "132.07" }
                        ]
                    },
                    {
                        "name": "2023第四季度",
                        "ch": [
                            { "name": "价格", "value": "386.39" },
                            { "name": "指数", "value": "132.07" }
                        ]
                    },
                    {
                        "name": "2024第一季度",
                        "ch": [
                            { "name": "价格", "value": "383.09" },
                            { "name": "指数", "value": "130.94" }
                        ]
                    },
                    {
                        "name": "2024第二季度",
                        "ch": [
                            { "name": "价格", "value": "383.14" },
                            { "name": "指数", "value": "130.96" }
                        ]
                    } 
            ]
    },
    mounted: function () {
        this.loadChatView();
        this.buildData();
    },
    methods: {
        //数据组合
        buildData: function () {
            var length = 11;
            this.List = [];
            for (var i = 0; i < this.RgList.length; i += length) {
                var arr = this.RgList.slice(i, i + length);
                this.List.push(arr);
            }
        },
        //加载图
        loadChatView: function () {
            var _this = this;
            var data = [];
            var months = [];
            var first = _this.RgList;
         
            first.forEach(function (firstitem) {
                months.push(firstitem.name);
                data.push(firstitem.ch[1].value);
            });

            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('main'));
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: _this.title + "指数指标趋势图",
                    x: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'line'
                    }
                },
                legend: {
                    data: [_this.title + '指数指标'],
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
                        name: _this.title + '指数指标',
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