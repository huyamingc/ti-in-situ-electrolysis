(function () {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();

  // ---------- Chart 1: energy ladder ----------
  var el1 = document.getElementById('chart-energy');
  if (el1) {
    var c1 = echarts.init(el1, null, { renderer: 'svg' });
    var cats = ['理论最低\n(2.729 V)', 'η=0.85\nV=3.5', 'η=0.80\nV=4.0', '总外部\n输入', '净能耗\n(论文值)', 'MC 中位数', 'MC P95'];
    var vals = [6112, 9222, 11198, 11233, 11191, 11780, 15361];
    var colors = [accent, accent, accent, accent, accent, accent2, accent2];
    c1.setOption({
      animation: false,
      grid: { left: 70, right: 30, top: 40, bottom: 60 },
      tooltip: {
        appendToBody: true,
        trigger: 'axis',
        formatter: function (p) {
          return p[0].name.replace(/\n/g, ' ') + '<br/>' + p[0].value.toLocaleString() + ' kWh/ton-Ti';
        }
      },
      xAxis: {
        type: 'category',
        data: cats,
        axisLabel: { color: muted, fontSize: 11, interval: 0, lineHeight: 15 },
        axisLine: { lineStyle: { color: rule } },
        axisTick: { show: false }
      },
      yAxis: {
        type: 'value',
        name: 'kWh/ton-Ti',
        nameTextStyle: { color: muted },
        axisLabel: { color: muted },
        splitLine: { lineStyle: { color: rule } }
      },
      series: [{
        type: 'bar',
        data: vals.map(function (v, i) { return { value: v, itemStyle: { color: colors[i] } }; }),
        barWidth: '55%',
        label: {
          show: true,
          position: 'top',
          color: ink,
          fontSize: 11,
          fontFamily: 'IBM Plex Mono, Consolas, monospace',
          formatter: function (p) { return p.value.toLocaleString(); }
        },
        markLine: {
          silent: true,
          symbol: 'none',
          data: [{
            yAxis: 14000,
            lineStyle: { color: accent2, type: 'dashed', width: 1.5 },
            label: {
              formatter: 'P(W<14,000)=85.8%',
              color: accent2,
              fontSize: 11,
              position: 'insideEndTop'
            }
          }]
        }
      }]
    });
    window.addEventListener('resize', function () { c1.resize(); });
  }

  // ---------- Chart 2: Spearman comparison ----------
  var el2 = document.getElementById('chart-spearman');
  if (el2) {
    var c2 = echarts.init(el2, null, { renderer: 'svg' });
    c2.setOption({
      animation: false,
      grid: { left: 60, right: 30, top: 50, bottom: 45 },
      legend: {
        data: ['论文声称值', '独立复算值'],
        textStyle: { color: muted },
        top: 8
      },
      tooltip: { appendToBody: true, trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: ['η_I (vs W_net)', 'V_cell (vs W_net)', 'ε (vs t)', 'τ (vs t)'],
        axisLabel: { color: muted, fontSize: 12 },
        axisLine: { lineStyle: { color: rule } },
        axisTick: { show: false }
      },
      yAxis: {
        type: 'value',
        min: -1,
        max: 1,
        axisLabel: { color: muted },
        splitLine: { lineStyle: { color: rule } }
      },
      series: [
        {
          name: '论文声称值',
          type: 'bar',
          data: [-0.85, 0.50, -0.68, 0.52],
          barWidth: '28%',
          itemStyle: { color: accent },
          label: { show: true, position: 'outside', color: ink, fontSize: 11 }
        },
        {
          name: '独立复算值',
          type: 'bar',
          data: [-0.849, 0.499, -0.672, 0.521],
          barWidth: '28%',
          itemStyle: { color: accent2, opacity: 0.55 },
          label: { show: true, position: 'outside', color: muted, fontSize: 11 }
        }
      ]
    });
    window.addEventListener('resize', function () { c2.resize(); });
  }
})();
