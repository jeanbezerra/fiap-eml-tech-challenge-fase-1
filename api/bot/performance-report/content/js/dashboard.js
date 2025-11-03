/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 100.0, "KoPercent": 0.0};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.18397727272727274, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [0.03744939271255061, 500, 1500, "1.3 - GET - /api/v1/books/filters?title=&category="], "isController": false}, {"data": [0.20756646216768918, 500, 1500, "1.4 - GET - /api/v1/health/"], "isController": false}, {"data": [0.19609856262833675, 500, 1500, "2.1 - GET - /api/v1/stats/overview"], "isController": false}, {"data": [0.03278688524590164, 500, 1500, "1.5 - GET - /api/v1/books"], "isController": false}, {"data": [0.22210743801652894, 500, 1500, "2.4 - GET - /api/v1/books/price-range?min_price=0&max_price=20"], "isController": false}, {"data": [0.20242914979757085, 500, 1500, "1.1 - GET - /api/v1/books/categories"], "isController": false}, {"data": [0.27125506072874495, 500, 1500, "1.2 - GET - /api/v1/books/id/{id}"], "isController": false}, {"data": [0.24020618556701032, 500, 1500, "2.2 - GET - /api/v1/stats/categories"], "isController": false}, {"data": [0.24742268041237114, 500, 1500, "2.3 - GET - /api/v1/books/best-rated?limit=10"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 4400, 0, 0.0, 1925.1268181818184, 583, 44076, 2057.0, 3143.8, 3544.0, 4143.919999999998, 4.874125703701899, 478.026307392484, 0.8150746322804483], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["1.3 - GET - /api/v1/books/filters?title=&category=", 494, 0, 0.0, 2720.9089068825915, 774, 44076, 2419.0, 3764.5, 3962.0, 4635.450000000001, 0.5481069230120583, 210.11919262546544, 0.09581165939370942], "isController": false}, {"data": ["1.4 - GET - /api/v1/health/", 489, 0, 0.0, 1682.6400817995927, 585, 3976, 2016.0, 2477.0, 2685.0, 3057.2000000000053, 0.5454472444317533, 0.20241206336334597, 0.08309547864389992], "isController": false}, {"data": ["2.1 - GET - /api/v1/stats/overview", 487, 0, 0.0, 1874.8357289527714, 774, 3658, 2214.0, 2658.8, 2776.6, 3208.12, 0.5434612792208082, 0.33435606045811445, 0.0865079965947185], "isController": false}, {"data": ["1.5 - GET - /api/v1/books", 488, 0, 0.0, 2867.4815573770497, 1040, 7036, 2969.5, 3991.1, 4264.749999999999, 4745.670000000001, 0.5436399143098726, 220.8966091643987, 0.08175834648800817], "isController": false}, {"data": ["2.4 - GET - /api/v1/books/price-range?min_price=0&max_price=20", 484, 0, 0.0, 1941.861570247933, 610, 4035, 1706.5, 2907.5, 3132.0, 3411.499999999999, 0.5448161977007406, 43.25714259557922, 0.10162099000082173], "isController": false}, {"data": ["1.1 - GET - /api/v1/books/categories", 494, 0, 0.0, 1664.4817813765192, 586, 3477, 2003.5, 2335.0, 2513.75, 2850.05, 0.5501897820624766, 0.5329963513730243, 0.08865362699248891], "isController": false}, {"data": ["1.2 - GET - /api/v1/books/id/{id}", 494, 0, 0.0, 1476.2348178137668, 583, 3295, 1200.0, 2322.5, 2487.5, 2840.5500000000006, 0.5496039847401452, 0.3289175416013502, 0.10412419242147283], "isController": false}, {"data": ["2.2 - GET - /api/v1/stats/categories", 485, 0, 0.0, 1559.7896907216495, 583, 2997, 1955.0, 2331.8, 2525.0, 2848.1399999999994, 0.5434143226088368, 2.2521976417499063, 0.08756187815474423], "isController": false}, {"data": ["2.3 - GET - /api/v1/books/best-rated?limit=10", 485, 0, 0.0, 1532.7195876288647, 585, 3383, 1522.0, 2337.8, 2478.1, 2896.9999999999986, 0.54331266131345, 2.4279284552444795, 0.09232070612162138], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": []}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 4400, 0, "", "", "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
