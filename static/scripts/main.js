let mm = 12;
let dd = 10;
let yyyy = 2020;

let mm2 = 12;
let dd2 = 24;
let yyyy2 = 2020;
Data = new Date();
Year = Data.getFullYear();
Month = Data.getMonth()+1;
Day = Data.getDate();
let datem = [Year, Month, Day];
let date2m = [2020, 12, 24];
let date = `${Year}-${Month}-${Day}`
let date2 = '2020-12-24'
let itWasClicked = 0;
let itWasClicked1 = 0;
datepickerDefault = new MtrDatepicker({
    target: "demo1",
    hours: null,
    targetElement: null,
    months: {
      min: 0,
      max: 11,
      step: 1,
      maxlength: 2
    },
    years: {
      min: 2020,
      max: 2021,
      step: 1,
      maxlength: 4
    },

    transitionDelay: 100,
    transitionValidationDelay: 500,
    references: { // Used to store references to the main elements
      hours: null
    },

    monthsNames: {
      0: "Jan",
      1: "Feb",
      2: "Mar",
      3: "Apr",
      4: "May",
      5: "Jun",
      6: "Jul",
      7: "Aug",
      8: "Sep",
      9: "Oct",
      10: "Nov",
      11: "Dec",
    },

    daysNames: {
      0: "",
      1: "",
      2: "",
      3: "",
      4: "",
      5: "",
      6: "",
    },

  timezones: null
});
$('.l_to').autocomplete({
  serviceUrl: 'service/autocomplete.ashx', // Страница для обработки запросов автозаполнения
  minChars: 1, // Минимальная длина запроса для срабатывания автозаполнения
  delimiter: /(,|;)\s*/, // Разделитель для нескольких запросов, символ или регулярное выражение
  maxHeight: 100, // Максимальная высота списка подсказок, в пикселях
  width: 150, // Ширина списка
  zIndex: 9999, // z-index списка
  deferRequestBy: 0, // Задержка запроса (мсек), на случай, если мы не хотим слать миллион запросов, пока пользователь печатает. Я обычно ставлю 300.
  params: { country: 'Yes'}, // Дополнительные параметры
  onSelect: function(data, value){ }, // Callback функция, срабатывающая на выбор одного из предложенных вариантов,
  lookup: ['Анапа','Архангельск','Белгород','Калуга','Нальчик','Орск','Псков','Ростов-на-Дону','Рязань','Тюмень','Ярославль','Чита','Грозный','Воркута','Абакан','Киров', 'Самара', 'Саратов','Ульяновск', 'Москва','Сургут','Казань','Норильск','Белгород','Ижевск','Пермь','Мурманск','Красноярск','Севастополь','Феодосия'] // Список вариантов для локального автозаполнения
});
$('.l_from').autocomplete({
  serviceUrl: 'service/autocomplete.ashx', // Страница для обработки запросов автозаполнения
  minChars: 1, // Минимальная длина запроса для срабатывания автозаполнения
  delimiter: /(,|;)\s*/, // Разделитель для нескольких запросов, символ или регулярное выражение
  maxHeight: 100, // Максимальная высота списка подсказок, в пикселях
  width: 150, // Ширина списка
  zIndex: 9999, // z-index списка
  deferRequestBy: 0, // Задержка запроса (мсек), на случай, если мы не хотим слать миллион запросов, пока пользователь печатает. Я обычно ставлю 300.
  params: { country: 'Yes'}, // Дополнительные параметры
  onSelect: function(data, value){ }, // Callback функция, срабатывающая на выбор одного из предложенных вариантов,
  lookup: ['Анапа','Архангельск','Белгород','Калуга','Нальчик','Орск','Псков','Ростов-на-Дону','Рязань','Тюмень','Ярославль','Чита','Грозный','Воркута','Абакан','Киров', 'Самара', 'Саратов','Ульяновск', 'Москва','Сургут','Казань','Норильск','Белгород','Ижевск','Пермь','Мурманск','Красноярск','Севастополь','Феодосия'] // Список вариантов для локального автозаполнения
});



datepickerDefault = new MtrDatepicker({
    target: "demo2",
    hours: null,
    years: {
      min: 2020,
      max: 2021,
      step: 1,
      maxlength: 4
    },
});

  /**Изменение даты вылета*/

$('#demo1').on('click', function() {
  itWasClicked1 = 1;
  mm2 = (parseInt($('.months').val())+1) > 12 ? 12 : parseInt($('.months').val())+1;
  dd = parseInt($('.dates').val());
  yyyy = parseInt($('.years').val());
  date = `${yyyy}-${mm}-${dd}`;//переменная для тебя для отправки в стринговом формате
  datem = [yyyy, mm, dd];//Переменная для меня, для валидации
});

/**Изменение даты возврата*/

$('#demo2').on('click', function() {
    itWasClicked = 1;
    mm2 = (parseInt($('#demo2 .months').val())+1) > 12 ? 12 : parseInt($('#demo2 .months').val())+1;
    dd2 = parseInt($('#demo2 .dates').val());
    yyyy2 = parseInt($('#demo2 .years').val());
    date2 = `${yyyy2}-${mm2}-${dd2}`; //переменная для тебя для отправки в стринговом формате
    date2m = [yyyy2, mm2, dd2]; //Переменная для меня, для валидации
});

/**Сравнение дат*/
function comporator(date1, date2){
    let dater1 = date1[0]*100+100*date1[1]+date1[2];
    let dater2 = date2[0]*100+100*date2[1]+date2[2];
    if (dater2 > dater1 || date2[0] > date1[0]){
        return true;
    } else{
        return false;
    }
}

/**Отправка значений с инпутов*/
var cityFrom = 0;
var cityTo = 0;
var dateForMaxin = 0;
var dateForMaxout = 0;
$('.submit').on('click', ()=>{
    if ($('.l_from').val() =="" || $('.l_to').val() ==""){
        Swal.fire({
            icon: 'error',
            title: 'Ошибка',
            text: 'Введите пункт отправления/назначения'
          })
        $('.swal2-shown').css({
            width:'100vw',
            height: '100vh'

        })
    }
    else{
        if (itWasClicked1 == 0){
          datem[2] = datem[2]+14;
          if (datem[2] > 31){
            datem[2] = datem[2]-14;
            datem[1] = datem[1]+1;
          }
          if (datem[1] > 12){
            datem[1] = datem[1]-12;
            datem[0] = datem[0]+1;
          
          }
          date = `${datem[0]}-${datem[1]}-${datem[2]}`
        }
        if (itWasClicked == 0){
          date2m[2] = datem[2]+1;
          if (date2m[2] > 31){
            date2m[2] = date2m[2]-1;
            date2m[1] = date2m[1]+1;
          }
          if (date2m[1] > 12){
            date2m[1] = date2m[1]-12;
            date2m[0] = date2m[0]+1;
          
          }
          date2 = `${date2m[0]}-${date2m[1]}-${date2m[2]}`
          console.log(date2m)
          console.log(datem)
        }
        if (!comporator(datem, date2m)){
            Swal.fire({
                icon: 'error',
                title: 'Ошибка',
                text: 'Несоответствие дат'
            })
            $('.swal2-shown').css({
                width:'100vw',
                height: '100vh'
    
            })
            
        } else {
            /**если даты соответствую и поля не пустые получаем значения городов с формы*/
            dateForMaxin = date;
            dateForMaxout = date2;
            cityFrom = cityValidator($('.l_from').val());
            k1 = prov_nachisla(cityFrom);
            cityTo = cityValidator($('.l_to').val());
            k2 = prov_nachisla(cityTo);
            if( k1 && k2){
              $('.finder').css({
                  transform: 'scale(0)',
              });
              $('body').css({
                background: 'linear-gradient(0deg,#ff6767 -20%, #7996ff 100%), url(assets/map.jpg)',
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                backgroundRepeat: 'no-repeat',
              });
              setTimeout(()=>{
                $('.finder').css({
                  opacity: '0'
                })
              },150);
              setTimeout(()=>{
                $('.loading').css({
                  transform: 'scale(1.2)',
                  opacity: '100'
                })
              },200);
              setTimeout(()=>{
                $('.loading').css({
                  transform: 'scale(1)',
                })
              },801);
              getReturnInform();
              
            }
          }
    }
    
    
})
/**Исправление регистра городов */
function cityValidator(city){
    let recity = city[0].toUpperCase()+city.slice(1);
    return recity;
} 



function getReturnInform() {
  console.log(dateForMaxin);
  console.log(dateForMaxout);
  console.log(cityFrom);
  console.log(cityTo);
  if(dateForMaxin != 0 && dateForMaxout != 0 && cityFrom != 0 && cityTo != 0 && k1!=0 && k2 !=0){
    $.getJSON (
    "/get_ret_inf",
    {
      "dateIn": dateForMaxin,
      "dateOut": dateForMaxout,
      "cityIn": cityFrom,
      "cityOut": cityTo
    },
    function (data) {
      console.log(data);
      setTimeout(()=>{
        $('.loading').css({
          opacity: '0',
          transform: 'scale(0)'
        })
      },150);
      setTimeout(()=>{
        $('.results').css({
          transform: 'scale(1.2)',
          zIndex: '10000',
          opacity: '100'
        });
      },200);
      setTimeout(()=>{
        $('.results').css({
          transform: 'scale(1)',
          zIndex: '10000',
        });
      },801);
      data = JSON.parse(data);
      console.log(data)
    let hostel = data.hostels.hotel;
    let hprice = data.hostels.price;
    let ticketsC =  data.tickets.aeroflot;
    let baggage =  data.tickets.baggage;
    let date_in =  data.tickets.date_in;
    let date_return = data.tickets.date_return;
    let price = data.tickets.price;
    let restoviv = `Отель: ${hostel}</br> Цена отеля: ${hprice} руб.</br> Авиакомания: ${ticketsC}</br> Багаж: ${baggage}</br> Дата вылета: ${date_in}</br> Дата возврата: ${date_return}</br> Стоимость: ${price} руб.`
    if(data.tickets == "nothing"){
        restoviv = "Введите адекватные города"
    }
    $('.res').html(restoviv);
    });
  }
}

//$(".submit").on("click", ()=>{
//  getReturnInform()
//})
function prov_nachisla(obj) 
{
  if (/[0-9]/.test(obj)) {
        Swal.fire({
          icon: 'error',
          title: 'Ошибка',
          text: 'Неверно введён город'
      })
      $('.swal2-shown').css({
          width:'100vw',
          height: '100vh'

      });
        return false;
        
  }
  else {
        return true;
  }
}

function re() {
    location.reload();
}