(self.webpackChunkipybus=self.webpackChunkipybus||[]).push([[261,568],{760:(e,i,t)=>{var s=t(337),o=t(431),a=s.DOMWidgetModel.extend({defaults:o.extend(s.DOMWidgetModel.prototype.defaults(),{_model_name:"BaseModel",_view_name:"BaseView",_model_module:"ipybus",_view_module:"ipybus",_model_module_version:"0.1.2",_view_module_version:"0.1.2",value:"Base",variable:"ipybus_var"})}),d=s.DOMWidgetView.extend({render:function(){variable=this.model.get("variable"),window[variable]=this.model,this.value_changed(),this.model.on("change:value",this.value_changed,this),this.update()},value_changed:function(){var e=this.model.get("count");e++,this.model.set("count",e)}});e.exports={BaseModel:a,BaseView:d}},568:(e,i,t)=>{e.exports=t(760),e.exports.version=t(147).version},261:(e,i,t)=>{var s=t(568),o=t(337);e.exports={id:"ipybus:plugin",requires:[o.IJupyterWidgetRegistry],activate:function(e,i){i.registerWidget({name:"ipybus",version:s.version,exports:s})},autoStart:!0}},147:e=>{"use strict";e.exports={version:"0.1.1"}}}]);