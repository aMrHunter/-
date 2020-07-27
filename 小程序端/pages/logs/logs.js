const tf = require('@tensorflow/tfjs-layers')
const tfl = require('@tensorflow/tfjs-core')
// const regeneratorRuntime = require('regenerator-runtime')
// const model = require('@tensorflow-models/model')

Page({

  logs:[],
  sort:0,
  data: {
    back:"backimg",
    
    imgurl: "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1584731567461&di=ee6dad07218b0ccf5406c501036e4cac&imgtype=0&src=http%3A%2F%2Fphotocdn.sohu.com%2F20160122%2Fmp56069582_1453469794725_8.jpg",
  },
  onLoad: function (option) {
    
    const eventChannel = this.getOpenerEventChannel()
    // eventChannel.emit('acceptDataFromOpenedPage', { data: '456' });
    // eventChannel.emit('someEvent', { data: '123' });
    // 监听acceptDataFromOpenerPage事件，获取上一页面通过eventChannel传送到当前页面的数据
    eventChannel.on('acceptDataFromOpenerPage', data => {
      console.log(111)
      console.log(data)

      this.setData({
        // logs: data.data.split(/['，','。']/g)
        logs: data.data,//.replace(/['，','。']/g,'\n')
        sort: data.sort,
        abs: data.back,
        name:data.name,
        title:data.title

      });

    }
    )
    wx.showToast({
      title: "正在为您创作...\n可能要数十秒",
      icon: "loading",
      duration: 1000
    });

    // console.log(111)
    // console.log(this.data.abs)
    // 如果接收数据有非汉字返回首页

    var n = this.data.abs
    if (n == 1) {
      wx.showModal({
        title: '提示',
        showCancel: false,
        content: '输入中包含非汉字，请重新输入',
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
 
    wx.request({
      url: 'http://127.0.0.1:5000/index',
      method: 'post',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },

      data: {
        head: this.data.logs,
        sort: this.data.sort,
      },
      success: (res) => {
        // console.log(11111)
        wx.hideToast({

        })
        // console.log(this.data)
        this.setData({
          strings: res.data.body.replace(/['，','。','？']/g, '\n')
        });
      },
      fail(){
        wx.showModal({
          title: '提示',
          showCancel: false,
          content: '连接失败',
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

    })
    }
    console.log(option.data)


  }
})
