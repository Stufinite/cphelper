# 課程資料查詢API (API of Course code of Dept. and Time of Course)

此API可以直接查詢`系所的課程代碼`和`課程的上課時間`

## API usage and Results

API使用方式（下面所寫的是api的URL pattern）<br>
(Usage of API (pattern written below is URL pattern))：

1. *`/cphelper/get/CourseOfDept/?dept=<>&school=<>&grade=<Optional>`*  
  取得系所的課程代碼<br>
  (Get Course code of Dept Name.)：<br>

  Grade參數用來指定年級，如果不加則是回傳所有年級的必選修：
  - 全年級：`/cphelper/get/CourseOfDept/?dept=多媒&school=NSYSU`
    - Result：

    ```
    {
      "obligatory": {
        "一１": [
          "D16149",
          "D16150",
          "D16148",
          "D16152",
          "D16151",
          "D16143",
          "D18798",
          "D16146",
          "D16147",
          "D16142",
          "D16144",
          "D16145"
        ],
        "四１": [
          "D16182",
          "D16180",
          "D16181"
        ]
      },
      "optional": {
        "二１": [
          "D16154",
          "D16155",
          "D16156",
          "D16158"
        ]
      }
    }
    ```

  - 指定年級：`/cphelper/get/CourseOfDept/?dept=多媒&school=NSYSU&grade=三１`
    - result：

    ```
    {
      "obligatory": {
        "三１": [
          "D16176",
          "D16173",
          "D16174",
          "D16175"
        ]
      },
      "optional": {
        "三１": [
          "D16164",
          "D16166",
          "D16169",
          "D16170",
          "D16168"
        ]
      }
    }
    ```

2. *`/cphelper/get/CourseOfTime/?day=<星期幾>&time=<第幾節課>&school=<學校名稱>&dept=<系所，可以是複數>`*  
查詢該時段有什麼課可以上：

  - 範例 (Example)：`cphelper/get/CourseOfTime/?day=1&time=5&school=NSYSU&dept=通識類+多媒`  
  代表是要查詢通識類和多媒該時段的課程  
  - *`dept`* ：如果要使用複數的時候，請記得用 *`+`* 把參數隔開
  - result：

    ```
    ["1159", "2217", "3432", "3434", "3445", "3447", "3448", "3449", "3450", "3451", "3452", "3453", "3456", "3457", "3458", "3459", "3460", "3461"]
    ```

3. *`/cphelper/get/Genra/?school=<學校名稱>`*  
該學校所有的系所和年級：

  - 範例 (Example)：`/cphelper/get/Genra/?school=NSYSU`  
  - result：

    ```
    {
      "其他類": {
        "語言": [
          "一１",
          "二１",
          "二２"
        ]
      },
      "通識類": {
        "通識": [
          "二２",
          "二１",
          "二５",
          "二３",
          "二４",
          "三Ｂ"
        ]
      },
      "體育類": {
        "體育": [
          "二２",
          "二１",
          "二３",
          "二４",
          "三Ａ",
          "三１",
          "四丁",
          "四丙",
          "四己"
        ]
      },
      "大學部": {
        "應中": [
          "一１",
          "二１",
          "三１",
          "四１"
        ],
        "休閒": [
          "一１",
          "二１",
          "三１",
          "四１"
        ],
        "美容系技優班": [
          "一１"
        ],
        "資應菁英班": [
          "一甲",
          "二甲",
          "三Ａ",
          "三甲",
          "四Ａ",
          "四甲",
          "五甲"
        ]
        ...
        ...
        ...
      }
    }
    ```

## Running & Testing

## Run

1. 插入mongodb以及django資料庫的範例指令：
    * 首先需要執行課程的爬蟲:[CampassCrawler](https://github.com/stufinite/campasscrawler)
    * `python manage.py buildCourse 學校genra.json 學校course.json 學校 第幾學年度`
    * 以中山大學為範例：`python manage.py buildCourse  NSYSU.json NSYSU 1061`
2. Execute : `python manage.py runserver`.

# test

需要注意，一定要先執行才能夠通過test，因為測試的資料要用才能匯入
test cmd:`python manage.py test cphelper`