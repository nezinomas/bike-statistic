$(function () {
    const chartData = JSON.parse(
        document.getElementById('chart-overall-data').textContent
    );
    Highcharts.setOptions({
        lang: {
            thousandsSep: '.',
            decimalPoint: '.',
        }
    });
    Highcharts.chart("chart-overall", {
        chart : {
            type: 'column',
            spacingRight: 0,
        },
        xAxis: {
            categories: chartData.categories,
            labels: {
                style: {
                    fontSize: '10px',
                },
            }
        },
        title: {
            text: ''
        },
        yAxis: {
            title: '',
            opposite: true,
            labels: {
                style: {
                    fontSize: '10px',
                },
            }
        },
        legend: {
            align: 'center',
            verticalAlign: 'bottom',
            shadow: false,
            reversed: true,
            layout: 'horizontal',
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
                borderRadius: 0,
            }
        },
        series: chartData.data,
    });
});
