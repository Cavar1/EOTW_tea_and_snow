import { baseAPIURL, baseStaticURL } from "../../config/config";

// pages/item_intro/item_intro.js
Page({

  data: {
    baseStaticURL:baseStaticURL,
    item:{}
  },

  onLoad(options) {
    let req=()=>{
      wx.request({
        url:baseAPIURL+"/api/tea-items/"+options.id,
        method:"GET",
        success:(res)=>{
          this.setData({
            item:res.data.data
          })
        },
        fail:(res)=>{
          console.log(res)
          req()
        }
      })
    }
    req()
  },

})