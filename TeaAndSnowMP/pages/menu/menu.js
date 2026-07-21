import { baseAPIURL, baseStaticURL } from "../../config/config";

Page({

  data:{
    baseStaticURL:baseStaticURL,
    token:"",
    // 菜单列表
    itemGroupList:null,
    // 当前选中的茶点组
    activeGroupIndex:0,
    // 右侧滚动目标
    scrollIntoView:"",
    // 购物车窗口
    isShowCart:false,
    // 购物车
    cartItemList:[],
    cartItemCount:0,
    totalPrice:"0"
  },

  // 点击左侧茶点组
  onGroupTap(e){
    const index=e.currentTarget.dataset.index
    this.setData({
      activeGroupIndex:index,
      scrollIntoView:'group'+index
    })
  },

  // 首次进入页面时
  onLoad(){
    // 获取token
    this.setData({
      token:wx.getStorageSync("token")
    })
  },

  // 进入页面时
  onShow(){
    // 获取菜单
    wx.request({
      url:baseAPIURL+"/api/menu",
      method:"GET",
      success:(res)=>{
        this.setData({
          itemGroupList:res.data.data
        })
      }
    })
    // 刷新购物车
    this.refreshCart()
  },

  // 点击物品卡片时
  onClickItemInfo(e){
    console.log(e)
    let id=e.currentTarget.dataset.id
    wx.navigateTo({
      url:"/pages/item_intro/item_intro?id="+id
    })
  },

  // 点击购物车bar时
  onClickCartBar(){
    this.setData({
      isShowCart:!this.data.isShowCart
    })
  },

  // 点击下单按钮时
  goToOrder(){
    wx.showModal({
      title: '点单',
      content: '确定下单吗？',
      confirmText:"下单！",
      confirmColor:"#5aa800",
      success :(res)=> {
        if (res.confirm) {
          this.requestCart({
            loadingTitle:"下单中",
            method:"POST",
            id:"/checkout",
            success:(res)=>{
              wx.navigateTo({
                url:"/pages/order/order?orderId="+res.data.data.order_no
              })
            }
          })
        }
      }
    })
  },

  // 关于购物车的请求
  requestCart({loadingTitle="加载中", method="GET",id="" ,body=null, success, fail}){
    wx.showLoading({
      title:loadingTitle,
      mask:true
    })
    wx.request({
      url:baseAPIURL+"/api/cart"+id,
      method:method,
      header:{"Authorization":this.data.token},
      data:body,
      success:(res)=>{
        console.log(res)
        wx.hideLoading()
        if (typeof success === "function") {
          success(res)
        }
      },
      fail:()=>{
        setTimeout(()=>{
          wx.hideLoading()
          this.refreshCart()
        },500)
        if (typeof fail === "function") {
          fail()
        }
      }
    })
  },
  // 刷新购物车
  refreshCart(){
    this.requestCart({
      loadingTitle:"加载中",
      method:"GET",
      body:null,
      success:(res)=>{
        let cartItemList=res.data.data.items
        let cartItemCount=0
        for(let i=0;i<cartItemList.length;i++){
          cartItemCount+=cartItemList[i].quantity
        }
        this.setData({
          cartItemList:cartItemList,
          cartItemCount:cartItemCount,
          totalPrice:res.data.data.total_price
        })
      }
    })
  },
  // 向购物车添加物品
  addToCart(e){
    this.requestCart({
      loadingTitle:"添加中",
      method:"POST",
      body:{
        "tea_item_id": e.target.dataset.id,
        "quantity": 1
      },
      success:()=>{this.refreshCart()}
    })
  },
  // 向购物车添加已有物品
  addMoreToCart(e){
    this.requestCart({
      loadingTitle:"添加中",
      method:"PUT",
      id:"/"+e.target.dataset.id,
      body:{
        "quantity":e.target.dataset.qtt+1
      },
      success:()=>{this.refreshCart()}
    })
  },
  // 删减购物车物品
  cutCart(e){
    let id=e.target.dataset.id
    let qtt=e.target.dataset.qtt
    if(qtt<=1){
      this.requestCart({
        loadingTitle:"丢弃中",
        method:"DELETE",
        id:"/"+id,
        success:()=>{this.refreshCart()}
      })
    }else{
      this.requestCart({
        loadingTitle:"减少中",
        method:"PUT",
        id:"/"+id,
        body:{
          "quantity":qtt-1
        },
        success:()=>{this.refreshCart()}
      })
    }
  },
})