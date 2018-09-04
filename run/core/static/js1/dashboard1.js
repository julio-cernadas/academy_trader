 $(document).ready(function () {
     // toat popup js
     $.toast({
         heading: 'Welcome to Capitalism',
         text: 'Remember: Greed is Good!',
         position: 'top-right',
         loaderBg: '#398fe5',
         icon: 'icon',
         hideAfter: 3000,
         stack: 1
     })


     //ct-visits
     new Chartist.Line('#ct-visits', {
         labels: ['12-08-2008', '12-07-2009', '12-10-2010', '2011', '2012', '2013', '2014', '2015', '2016', '2018', 'T'],
         series: [[],[5, 2, 7, 4, 5, 3, 5, 4, 5, 3, 1]]
     }, {
         showPoint: true,
         fullWidth: true,
         plugins: [
    Chartist.plugins.tooltip()
  ],
         axisY: {
             labelInterpolationFnc: function (value) {
                 return '$'+(value);
             }
         },
         showArea: true
     });

     // counter
     $(".counter").counterUp({
         delay: 100,
         time: 900
     });

     var sparklineLogin = function () {
         $('#sparklinedash').sparkline([6, 8, 7, 10, 8, 10, 9, 11], {
             type: 'bar',
             height: '30',
             barWidth: '4',
             resize: true,
             barSpacing: '5',
             barColor: '#008738'
         });
         $('#sparklinedash2').sparkline([6, 8, 7, 10, 8, 10, 9, 11], {
             type: 'bar',
             height: '30',
             barWidth: '4',
             resize: true,
             barSpacing: '5',
             barColor: '#008738'
         });
         $('#sparklinedash3').sparkline([6, 8, 7, 10, 8, 10, 9, 11], {
             type: 'bar',
             height: '30',
             barWidth: '4',
             resize: true,
             barSpacing: '5',
             barColor: '#008738'
         });
         $('#sparklinedash4').sparkline([11, 9, 10, 8, 10, 7, 8, 6], {
             type: 'bar',
             height: '30',
             barWidth: '4',
             resize: true,
             barSpacing: '5',
             barColor: '#ff1e1e'
         });
         $('#sparklinedash5').sparkline([6, 8, 7, 10, 8, 10, 9, 11], {
             type: 'bar',
             height: '30',
             barWidth: '4',
             resize: true,
             barSpacing: '5',
             barColor: '#008738'
         });
     }
     var sparkResize;
     $(window).on("resize", function (e) {
         clearTimeout(sparkResize);
         sparkResize = setTimeout(sparklineLogin, 500);
     });
     sparklineLogin();
 });
