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
  curveBasis
} from 'd3';

const svg = select('svg');

const height = +svg.attr('height');
const width = +svg.attr('width');

const render = data => {

  const xValue = d => d.timestamp;
  const yValue = d => d.temperature; 
  
  //常量参数设置
  const circleRadius =7;
  const xAxisLabel = 'Time'
  const yAxisLabel = 'Temperature'
  const title = 'Temperature as Time'
  
  //画布
  const margin = {top: 70, right: 40, bottom: 80, left: 80};
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
 
  const xScale = scaleTime()  	
  	.domain(extent(data,xValue))
  	.range([0, innerWidth])
  	.nice();
  
  const yScale = scaleLinear()
  	.domain(extent(data,yValue))
  	//y轴从小到大排列(最小的数据映射到y坐标最大的地方，因为svg画布默认屏幕上方为y轴起始点，往下为y轴正方向。所以如果要绘制的y轴有从下往上的排列关系的话，就要反向映射)
  	.range([innerHeight,0])
  	.nice();
  
  const g = svg.append('g')
  	.attr('transform', `translate(${margin.left}, ${margin.top})`);
   
  
  const xAxis = axisBottom(xScale)
  	.tickSize(-innerHeight)
  	.tickPadding(20);
  
  
  const xAxisG = g.append('g').call(xAxis)
  	.attr('transform', `translate(0, ${innerHeight})`);
  
  xAxisG.select('.domain').remove();
	xAxisG.append('text').text(xAxisLabel)
    .attr('y',60)
    .attr('x',innerWidth/2)
    .attr('fill','black')
    //text-anchor设置文本居中
  	.attr('text-anchor','middle')
  	.attr('class','axis-label')
 
  
  
  const yAxis = axisLeft(yScale)
  	.tickSize(-innerWidth)
  	.tickPadding(10)
  
  const yAxisG = g.append('g').call(yAxis);
  yAxisG.selectAll('.domain').remove();
  yAxisG.append('text').text(yAxisLabel)
    .attr('fill','black')
  	.attr('class','axis-label')
    .attr('transform','rotate(-90)')
  	.attr('y',-40)
  	.attr('x',-innerHeight/2)
  	.attr('text-anchor','middle')
  
  
  
  //画path,返回一个构造函数
  const lineGenerator = line()
  	//设置要连线的点的x和y坐标的值,x()传入一个映射规则构造函数
  	.x(d=>xScale(xValue(d)))
  	.y(d=>yScale(yValue(d)))
  	//让曲线变得更平滑,需要到库
  	.curve(curveBasis);
  
  
  g.append('path')
  	.attr('stroke','black')
  	.attr('class','line-path')
  	.attr('d',lineGenerator(data))
  
  //整体设置title
  g.append('text').text(title)
    .attr('y',-5)
  	.attr('text-anchor','middle')
  	.attr('x',innerWidth/2)
 
}


csv('https://vizhub.com/curran/datasets/temperature-in-san-francisco.csv')
  .then(data => {
  
	data.forEach(d => {
    //数据预处理，格式转换
    d.temperature = +d.temperature;
    d.timestamp = new Date(d.timestamp);
    
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
fill:none;
  stroke:maroon;
  stroke-width:5;
  stroke-linejoin:round;
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

Output

![折线图](C:\Users\DELL\Desktop\Python Work\Python Notepad\Python_数据可视化\折线图.png)





有关SVG属性的设置帮助文档

https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute



