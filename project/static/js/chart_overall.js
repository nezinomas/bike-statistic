$(function () {
    const chartData = JSON.parse(
        document.getElementById('chart-overall-data').textContent
    );
    Highcharts.setOptions({
        lang: {
            thousandsSep: '.',
            decimalPoint: ',',
        }
    });
    Highcharts.chart("chart-overall", {
        chart : { type: 'column'},
        xAxis: {
            categories: chartData.categories,
        },
        margin: 0,
        title: {
            text: ''
        },
        yAxis: {
            min: 0,
            title: {
                text: 'km, thousants'
            },
        },
        legend: {
            align: 'right',
            verticalAlign: 'middle',
            shadow: false,
            reversed: true,
            layout: 'vertical',
            itemMarginBottom: 10
        },
        tooltip: {
            pointFormat: '{point.y:,.0f}',
            formatter: function () {
                return '<b>' + this.x + '</b><br/>' +
                    `${this.series.name}: ${Highcharts.numberFormat(this.point.y, 0)}<br/>` +
                    `Total: ${Highcharts.numberFormat(this.point.stackTotal, 0)}`;
            }
        },
        plotOptions: {
            column: {
                stacking: 'normal',
            }
        },
        series: chartData.data,
    });
});
