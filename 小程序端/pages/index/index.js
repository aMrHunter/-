//index.js
//获取应用实例
const tfl = require('@tensorflow/tfjs-layers')
const tf = require('@tensorflow/tfjs-core')
Page({
  data:{
    // 诗的类别
    sort: 1,
    // 藏头诗和续写诗的输入
    name:[],
    title:[],
    head: [],
    url:['../../resources/img/logo.png','123'],
    inputValue: '',
    items:[
      { name: 1, value: '藏头诗', checked: true },
      { name: 2, value: '续写诗' },
      { name: 0, value: '自由诗 ' },

    ],
    // 禁用输入框
    cor: false,
    //占位符
    used: "请输入八个以内汉字",
    // 
    strings: [],
    // 包含非汉字标志
    navigate: 0,
  },
  // 接受输入框内容
  bindKeyInput: function (e) {
    this.setData({
      head: e.detail.value,
      navigate: 0
    })
  },
  bindKeyInput_title: function (e) {
    this.setData({
      title: e.detail.value,

    })
  },
  bindKeyInput_name: function (e) {
    this.setData({
      name: e.detail.value,
    })
  },
  // 选择作诗的类型
  radioChange: function (e) {
    console.log('radio发生change事件，携带value值为：', e.detail.value)
    this.setData({
      sort: e.detail.value, 
     // cor: e.detail.value, 
    });
    if(this.data.sort == 0){
      this.setData({
        used: "不用输入如何字",
        cor: true,
        //head:[],
        // cor: e.detail.value, 
      });
    }
    else{
      this.setData({
        used: "请输入八个以内汉字",
        cor: false,
      });
    }
    console.log(this.data.sort)

  },
  // 提交按钮事件 
  bindSubmitText: function(){

    var str = this.data.head
    var s = this.data.sort
    var name = this.data.name
    var title = this.data.title
      // 判断是否包含非数字
      //var reg = new RegExp("[\\u4E00-\\u9FFF]+", "g");
    if(name.length == 0 || title.length == 0){
      wx.showModal({
        title: '提示',
        showCancel: false,
        content: '请输入题目和作者',
        success(res) {
          if (res.confirm) {
            console.log('用户点击确定')
            wx.navigateBack({
              delta: 1,
            })
          }

        }
      })
    }
    else if ((s == 1 || s == 2)&& str.length == 0) {
      wx.showModal({
        title: '提示',
        showCancel: false,
        content: '请输入相关内容再重试',
        success(res) {
          if (res.confirm) {
            console.log('用户点击确定')
            wx.navigateBack({
              delta: 1,
            })
          }

        }
      })
    }
  else {



  
    
    if(s != 0){
      for (var i = 0; i < str.length; i++) {
        if (str.charCodeAt(i) < 19968 || str.charCodeAt(i) > 40869) {
          console.log("包含非汉字！");

          wx.showToast({
            title: "包含非汉字！",
            icon: "loading",
            duration: 100000
          });
          this.setData({
            navigate: 1
          });
        }
    }

        // if (reg.test(str[i])) { 
        //   console.log(str[i]);
 
        // }
        // else{
        //   console.log("包含非汉字！");    
        // }
      }

    // wx.showToast({
    //   title: "正在为您创作...\n可能要数十秒",
    //   icon: "loading",
    //   duration: 10000
    // });
    var chinese = this.data.navigate
    wx.hideToast({

    })
    // console.log(123321)
    // console.log(this.data.head)
    // console.log(this.data.strings)
          
      wx.navigateTo({
      duration: 2000,
      url: '../logs/logs',
      events: {   
      },
      
      success: function (res) {
        // 通过eventChannel向被打开页面传送数据
        // console.log(456)
        // console.log(str)
        res.eventChannel.emit('acceptDataFromOpenerPage', { 
          data: str,
          sort:s ,
          back : chinese,
          name :name,
          title:title
        })
      }
        
      })
  }
    
  },
  onLoad: function () {
    console.log('onLoad');
  },

 
})
