
// loadFooterPage()
async function loadPage() {
    // await fetch('/import_menu')
    //     .then(response => response.text())
    //     .then(data => {
    //         document.getElementById('content-container').innerHTML = data;
    //     })
    //     .catch(error => console.error('Error loading page:', error));


    try {
      const response = await fetch('/import_menu');
      if (!response.ok) throw new Error('페이지 로드 실패');
      
      const data = await response.text();
      $(".content-container").html(data)
    //   document.getElementById('content-container').innerHTML = data;
      
    } catch (error) {
      console.error(error);
    }
}

async function loadFooterPage() {
    try {
      const response = await fetch('/import_footer');
      if (!response.ok) throw new Error('페이지 로드 실패');
      
      const data = await response.text();
      document.getElementById('footer-container').innerHTML = data;

      
    } catch (error) {
      console.error(error);
    }
}


  
async function loadMobiscroll() {
    var now = new Date();
    var week = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 6);

    $("#start-picker,#end-picker").daterangepicker({
            autoUpdateInput: false, // 자동 입력 방지
            locale: {
                format: 'YYYY-MM-DD', // 날짜 형식 설정
                // applyLabel: '확인',
                // cancelLabel: '취소'
            }
        }, 
        function(start, end, label) {
            console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
        }
    );

    // 선택한 날짜를 input에 각각 적용
    $('#start-picker,#end-picker').on('apply.daterangepicker', function(ev, picker) {
        $('#start-picker').val(picker.startDate.format('YYYY-MM-DD'));
        $('#end-picker').val(picker.endDate.format('YYYY-MM-DD'));
    });

    // 취소 버튼 클릭 시 input 값 비우기
    $('#start-picker,#end-picker').on('cancel.daterangepicker', function() {
        $('#start-picker').val('');
        $('#end-picker').val('');
    });

    // $('#mobile-picker-input-start')
    // .mobiscroll()
    // .datepicker({
    //     controls: ['calendar'],
    //     select: 'range',
    //     showRangeLabels: true,
    //     touchUi: true,
    //     startInput: '#mobile-picker-input-start',
    //     endInput: '#mobile-picker-input-end'
    //     //dateFormat: 'YYYY-MM-DD' // 원하는 포맷으로 변경
    // });
    
    // var instance = $('#mobile-picker-button')
    // .mobiscroll()
    // .datepicker({
    //     controls: ['calendar'],
    //     select: 'range',
    //     showRangeLabels: true,
    //     showOnClick: false,
    //     showOnFocus: false,
    // })
    // .mobiscroll('getInst');

    // instance.setVal([now, week], true);

    // $('#mobile-picker-mobiscroll')
    // .mobiscroll()
    // .datepicker({
    //     controls: ['calendar'],
    //     select: 'range',
    //     showRangeLabels: true,
    // });

    // var inlineInst = $('#mobile-picker-inline')
    // .mobiscroll()
    // .datepicker({
    //     controls: ['calendar'],
    //     select: 'range',
    //     showRangeLabels: true,
    //     display: 'inline',
    // })
    // .mobiscroll('getInst');

    // inlineInst.setVal([now, week], true);

    // $('#show-mobile-date-picker').click(function () {
    // instance.open();
    // return false;
    // });
}

let calendar;
function loadFullCalendar(){
    let calendarEl = document.getElementById('calendar');

    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth', // 초기 화면 (월간 달력)        
    });
    calendar.setOption('locale', 'en');
    calendar.render();

    // $('#calendar').fullCalendar({
    //     header: {
    //       left: 'prev,next today',
    //       center: 'title',
    //     //   right: 'month,agendaWeek,agendaDay'
    //     right: 'month'
    //     },
    //     defaultView: 'month',
    //     editable: false,
    //     events: [
    //       {
    //         title: '이벤트 1',
    //         start: '2025-02-20'
    //       },
    //       {
    //         title: '이벤트 2',
    //         start: '2025-02-22',
    //         end: '2025-02-24'
    //       }
    //     ]
    // });
}

let openDB;
let storeName = "myStore"; // 객체 저장소 이    
let dbVersion = 4;
const dbName = "MyDatabase"; // 데이터베이스 이름

async function createDataBaseStore(storeName) {
    openDB = () => {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(dbName, dbVersion);

            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                // 객체 저장소 생성 (이미 존재하지 않으면)
                if (!db.objectStoreNames.contains("travelInfo")) {
                    db.createObjectStore(storeName, { keyPath: "id", autoIncrement: true });
                }

                 // 객체 저장소 생성 (이미 존재하지 않으면)
                 if (!db.objectStoreNames.contains("myStore")) {
                    db.createObjectStore(storeName, { keyPath: "id", autoIncrement: true });
                }
            };

            request.onsuccess = (event) => {
                resolve(event.target.result); // 데이터베이스 연결 성공
            };

            request.onerror = (event) => {
                reject("Error opening DB: " + event.target.errorCode);
            };
        });
    };
}

async function insertDataBaseStore(storeName , data){
    // 인덱스DB 저장
    openDB().then((db) => {
        const transaction = db.transaction([storeName], "readwrite");
        const store = transaction.objectStore(storeName);
    

        const request = store.add(data);

        request.onsuccess = () => {
            alert("데이터가 저장되었습니다!");
        };

        request.onerror = (event) => {
            alert("데이터 저장 실패: " + event.target.error);
        };
    }).catch((error) => {
        alert("DB 열기 실패: " + error);
    });
}