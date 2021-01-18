index.html

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Bar Chart Learning</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://unpkg.com/d3@6.3.1/dist/d3.min.js"></script>
  </head>
  <body>
    <svg width="960" height="500">
     
    </svg>
    <script src="bundle.js"></script>
  </body>
</html>
```

index.js

```javascript
import { 
  select, 
  csv, 
  scaleLinear, 
  scaleBand,
  scalePoint,
  max,
  axisLeft,
  axisBottom,
  format,
  extent,
  scaleTime,
  line,
  curveBasis,
  area
  
} from 'd3';

const svg = select('svg');

const height = +svg.attr('height');
const width = +svg.attr('width');

const render = data => {

  const xValue = d => d.year;
  const yValue = d => d.population; 
  
  //常量参数设置
  const circleRadius =7;
  const xAxisLabel = 'Time'
  const yAxisLabel = 'Population'
  const title = 'World Population'
  
  //画布
  const margin = {top: 70, right: 40, bottom: 80, left: 80};
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  //scaleTime用于时间数据映射
  const xScale = scaleTime()
  	.domain(extent(data,xValue))
  	.range([0, innerWidth])
  	.nice();
  

  const yScale = scaleLinear()
  	.domain([0,max(data,yValue)])
  	//y轴从小到大排列
  	.range([innerHeight,0])
  	.nice();
  
  const yAxisTickFormat = number=>format(".1s")(number).replace('T','B');
  
  
  
  
  const g = svg.append('g')
  	.attr('transform', `translate(${margin.left}, ${margin.top})`);
   
  
  //画area,返回一个构造函数,在坐标格式设置之前执行使得坐标格式悬浮在areachart上方
  const areaGenerator = area()
  	//设置x和y的值
  	.x(d=>xScale(xValue(d)))
  	//曲线的高的y的坐标位置
  	.y1(d=>yScale(yValue(d)))
  	//曲线的底部y坐标位置
  	.y0(innerHeight)
  	//让曲线变得更平滑
  	.curve(curveBasis);
  
  
  g.append('path')
  	.attr('stroke','black')
  	.attr('class','line-path')
  	.attr('d',areaGenerator(data))
  
  
  const xAxis = axisBottom(xScale)
    // .tickFormat(xAxisTickFormat)
  	.tickSize(-innerHeight)
  	//把tick远离坐标轴一些
  	.tickPadding(20)
  	.ticks(6);
  
  
  const xAxisG = g.append('g').call(xAxis)
  	.attr('transform', `translate(0, ${innerHeight})`);
  
  xAxisG.select('.domain').remove();
	xAxisG.append('text').text(xAxisLabel)
    .attr('y',60)
    .attr('x',innerWidth/2)
    .attr('fill','black')
  	.attr('text-anchor','middle')
  	.attr('class','axis-label')
 
  
  
  const yAxis = axisLeft(yScale)
  	.tickSize(-innerWidth)
  	.tickPadding(10)
  	.tickFormat(yAxisTickFormat)
  
  
  const yAxisG = g.append('g').call(yAxis);
  yAxisG.selectAll('.domain').remove();
  yAxisG.append('text').text(yAxisLabel)
    .attr('fill','black')
  	.attr('class','axis-label')
    .attr('transform','rotate(-90)')
  	.attr('y',-40)
  	.attr('x',-innerHeight/2)
  	.attr('text-anchor','middle')
  
  
  

  //整体设置title
  svg.append('text').text(title)
    .attr('y',45)
  	.attr('text-anchor','middle')
  	.attr('x',width/2)
 
}


csv('https://vizhub.com/curran/datasets/world-population-by-year-2015.csv')
  .then(data => {
  
	data.forEach(d => {
    console.log(data)
    //数据预处理，格式转换
    d.population = +d.population*1000; //数据是以千为单位，我们要自己调整
    d.year = new Date(d.year);//只有年份传入的话默认会解析成当年的第一天
    
  });
  render(data);
});
```

styles.css

```css
body {
  margin: 0;
  overflow: hidden;
}

circle {
	fill: steelblue;

}

.line-path{
	fill:maroon;
  
}
text {
	font-size: 1.5em;
  font-family:sans-serif;
  
}

.tick text{
	fill: #635F5D;

}

.axis-label {
font-size:2.5em;}
```

OutPut：

![AreaChart](C:\Users\DELL\Desktop\Python Work\Python Notepad\Python_数据可视化\AreaChart.png)

PS：append顺序会影响图元的展示顺序