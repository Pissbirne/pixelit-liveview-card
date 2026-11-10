function e(e,t,i,o){var s,n=arguments.length,a=n<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)a=Reflect.decorate(e,t,i,o);else for(var r=e.length-1;r>=0;r--)(s=e[r])&&(a=(n<3?s(a):n>3?s(t,i,a):s(t,i))||a);return n>3&&a&&Object.defineProperty(t,i,a),a}"function"==typeof SuppressedError&&SuppressedError;const t=globalThis,i=t.ShadowRoot&&(void 0===t.ShadyCSS||t.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,o=Symbol(),s=new WeakMap;let n=class{constructor(e,t,i){if(this._$cssResult$=!0,i!==o)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e,this.t=t}get styleSheet(){let e=this.o;const t=this.t;if(i&&void 0===e){const i=void 0!==t&&1===t.length;i&&(e=s.get(t)),void 0===e&&((this.o=e=new CSSStyleSheet).replaceSync(this.cssText),i&&s.set(t,e))}return e}toString(){return this.cssText}};const a=(e,...t)=>{const i=1===e.length?e[0]:t.reduce((t,i,o)=>t+(e=>{if(!0===e._$cssResult$)return e.cssText;if("number"==typeof e)return e;throw Error("Value passed to 'css' function must be a 'css' function result: "+e+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+e[o+1],e[0]);return new n(i,e,o)},r=i?e=>e:e=>e instanceof CSSStyleSheet?(e=>{let t="";for(const i of e.cssRules)t+=i.cssText;return(e=>new n("string"==typeof e?e:e+"",void 0,o))(t)})(e):e,{is:l,defineProperty:c,getOwnPropertyDescriptor:d,getOwnPropertyNames:h,getOwnPropertySymbols:p,getPrototypeOf:u}=Object,m=globalThis,g=m.trustedTypes,f=g?g.emptyScript:"",_=m.reactiveElementPolyfillSupport,v=(e,t)=>e,$={toAttribute(e,t){switch(t){case Boolean:e=e?f:null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let i=e;switch(t){case Boolean:i=null!==e;break;case Number:i=null===e?null:Number(e);break;case Object:case Array:try{i=JSON.parse(e)}catch(e){i=null}}return i}},b=(e,t)=>!l(e,t),y={attribute:!0,type:String,converter:$,reflect:!1,useDefault:!1,hasChanged:b};Symbol.metadata??=Symbol("metadata"),m.litPropertyMetadata??=new WeakMap;let x=class extends HTMLElement{static addInitializer(e){this._$Ei(),(this.l??=[]).push(e)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(e,t=y){if(t.state&&(t.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(e)&&((t=Object.create(t)).wrapped=!0),this.elementProperties.set(e,t),!t.noAccessor){const i=Symbol(),o=this.getPropertyDescriptor(e,i,t);void 0!==o&&c(this.prototype,e,o)}}static getPropertyDescriptor(e,t,i){const{get:o,set:s}=d(this.prototype,e)??{get(){return this[t]},set(e){this[t]=e}};return{get:o,set(t){const n=o?.call(this);s?.call(this,t),this.requestUpdate(e,n,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)??y}static _$Ei(){if(this.hasOwnProperty(v("elementProperties")))return;const e=u(this);e.finalize(),void 0!==e.l&&(this.l=[...e.l]),this.elementProperties=new Map(e.elementProperties)}static finalize(){if(this.hasOwnProperty(v("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(v("properties"))){const e=this.properties,t=[...h(e),...p(e)];for(const i of t)this.createProperty(i,e[i])}const e=this[Symbol.metadata];if(null!==e){const t=litPropertyMetadata.get(e);if(void 0!==t)for(const[e,i]of t)this.elementProperties.set(e,i)}this._$Eh=new Map;for(const[e,t]of this.elementProperties){const i=this._$Eu(e,t);void 0!==i&&this._$Eh.set(i,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const i=new Set(e.flat(1/0).reverse());for(const e of i)t.unshift(r(e))}else void 0!==e&&t.push(r(e));return t}static _$Eu(e,t){const i=t.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof e?e.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(e=>e(this))}addController(e){(this._$EO??=new Set).add(e),void 0!==this.renderRoot&&this.isConnected&&e.hostConnected?.()}removeController(e){this._$EO?.delete(e)}_$E_(){const e=new Map,t=this.constructor.elementProperties;for(const i of t.keys())this.hasOwnProperty(i)&&(e.set(i,this[i]),delete this[i]);e.size>0&&(this._$Ep=e)}createRenderRoot(){const e=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((e,o)=>{if(i)e.adoptedStyleSheets=o.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet);else for(const i of o){const o=document.createElement("style"),s=t.litNonce;void 0!==s&&o.setAttribute("nonce",s),o.textContent=i.cssText,e.appendChild(o)}})(e,this.constructor.elementStyles),e}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(e=>e.hostConnected?.())}enableUpdating(e){}disconnectedCallback(){this._$EO?.forEach(e=>e.hostDisconnected?.())}attributeChangedCallback(e,t,i){this._$AK(e,i)}_$ET(e,t){const i=this.constructor.elementProperties.get(e),o=this.constructor._$Eu(e,i);if(void 0!==o&&!0===i.reflect){const s=(void 0!==i.converter?.toAttribute?i.converter:$).toAttribute(t,i.type);this._$Em=e,null==s?this.removeAttribute(o):this.setAttribute(o,s),this._$Em=null}}_$AK(e,t){const i=this.constructor,o=i._$Eh.get(e);if(void 0!==o&&this._$Em!==o){const e=i.getPropertyOptions(o),s="function"==typeof e.converter?{fromAttribute:e.converter}:void 0!==e.converter?.fromAttribute?e.converter:$;this._$Em=o;const n=s.fromAttribute(t,e.type);this[o]=n??this._$Ej?.get(o)??n,this._$Em=null}}requestUpdate(e,t,i,o=!1,s){if(void 0!==e){const n=this.constructor;if(!1===o&&(s=this[e]),i??=n.getPropertyOptions(e),!((i.hasChanged??b)(s,t)||i.useDefault&&i.reflect&&s===this._$Ej?.get(e)&&!this.hasAttribute(n._$Eu(e,i))))return;this.C(e,t,i)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(e,t,{useDefault:i,reflect:o,wrapped:s},n){i&&!(this._$Ej??=new Map).has(e)&&(this._$Ej.set(e,n??t??this[e]),!0!==s||void 0!==n)||(this._$AL.has(e)||(this.hasUpdated||i||(t=void 0),this._$AL.set(e,t)),!0===o&&this._$Em!==e&&(this._$Eq??=new Set).add(e))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}const e=this.scheduleUpdate();return null!=e&&await e,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[e,t]of this._$Ep)this[e]=t;this._$Ep=void 0}const e=this.constructor.elementProperties;if(e.size>0)for(const[t,i]of e){const{wrapped:e}=i,o=this[t];!0!==e||this._$AL.has(t)||void 0===o||this.C(t,void 0,i,o)}}let e=!1;const t=this._$AL;try{e=this.shouldUpdate(t),e?(this.willUpdate(t),this._$EO?.forEach(e=>e.hostUpdate?.()),this.update(t)):this._$EM()}catch(t){throw e=!1,this._$EM(),t}e&&this._$AE(t)}willUpdate(e){}_$AE(e){this._$EO?.forEach(e=>e.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(e){return!0}update(e){this._$Eq&&=this._$Eq.forEach(e=>this._$ET(e,this[e])),this._$EM()}updated(e){}firstUpdated(e){}};x.elementStyles=[],x.shadowRootOptions={mode:"open"},x[v("elementProperties")]=new Map,x[v("finalized")]=new Map,_?.({ReactiveElement:x}),(m.reactiveElementVersions??=[]).push("2.1.2");const w=globalThis,A=e=>e,k=w.trustedTypes,E=k?k.createPolicy("lit-html",{createHTML:e=>e}):void 0,S="$lit$",C=`lit$${Math.random().toFixed(9).slice(2)}$`,R="?"+C,M=`<${R}>`,L=document,P=()=>L.createComment(""),H=e=>null===e||"object"!=typeof e&&"function"!=typeof e,O=Array.isArray,F="[ \t\n\f\r]",z=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,D=/-->/g,U=/>/g,N=RegExp(`>|${F}(?:([^\\s"'>=/]+)(${F}*=${F}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),T=/'/g,j=/"/g,I=/^(?:script|style|textarea|title)$/i,V=(e=>(t,...i)=>({_$litType$:e,strings:t,values:i}))(1),B=Symbol.for("lit-noChange"),W=Symbol.for("lit-nothing"),Y=new WeakMap,q=L.createTreeWalker(L,129);function Z(e,t){if(!O(e)||!e.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==E?E.createHTML(t):t}const K=(e,t)=>{const i=e.length-1,o=[];let s,n=2===t?"<svg>":3===t?"<math>":"",a=z;for(let t=0;t<i;t++){const i=e[t];let r,l,c=-1,d=0;for(;d<i.length&&(a.lastIndex=d,l=a.exec(i),null!==l);)d=a.lastIndex,a===z?"!--"===l[1]?a=D:void 0!==l[1]?a=U:void 0!==l[2]?(I.test(l[2])&&(s=RegExp("</"+l[2],"g")),a=N):void 0!==l[3]&&(a=N):a===N?">"===l[0]?(a=s??z,c=-1):void 0===l[1]?c=-2:(c=a.lastIndex-l[2].length,r=l[1],a=void 0===l[3]?N:'"'===l[3]?j:T):a===j||a===T?a=N:a===D||a===U?a=z:(a=N,s=void 0);const h=a===N&&e[t+1].startsWith("/>")?" ":"";n+=a===z?i+M:c>=0?(o.push(r),i.slice(0,c)+S+i.slice(c)+C+h):i+C+(-2===c?t:h)}return[Z(e,n+(e[i]||"<?>")+(2===t?"</svg>":3===t?"</math>":"")),o]};class J{constructor({strings:e,_$litType$:t},i){let o;this.parts=[];let s=0,n=0;const a=e.length-1,r=this.parts,[l,c]=K(e,t);if(this.el=J.createElement(l,i),q.currentNode=this.el.content,2===t||3===t){const e=this.el.content.firstChild;e.replaceWith(...e.childNodes)}for(;null!==(o=q.nextNode())&&r.length<a;){if(1===o.nodeType){if(o.hasAttributes())for(const e of o.getAttributeNames())if(e.endsWith(S)){const t=c[n++],i=o.getAttribute(e).split(C),a=/([.?@])?(.*)/.exec(t);r.push({type:1,index:s,name:a[2],strings:i,ctor:"."===a[1]?te:"?"===a[1]?ie:"@"===a[1]?oe:ee}),o.removeAttribute(e)}else e.startsWith(C)&&(r.push({type:6,index:s}),o.removeAttribute(e));if(I.test(o.tagName)){const e=o.textContent.split(C),t=e.length-1;if(t>0){o.textContent=k?k.emptyScript:"";for(let i=0;i<t;i++)o.append(e[i],P()),q.nextNode(),r.push({type:2,index:++s});o.append(e[t],P())}}}else if(8===o.nodeType)if(o.data===R)r.push({type:2,index:s});else{let e=-1;for(;-1!==(e=o.data.indexOf(C,e+1));)r.push({type:7,index:s}),e+=C.length-1}s++}}static createElement(e,t){const i=L.createElement("template");return i.innerHTML=e,i}}function G(e,t,i=e,o){if(t===B)return t;let s=void 0!==o?i._$Co?.[o]:i._$Cl;const n=H(t)?void 0:t._$litDirective$;return s?.constructor!==n&&(s?._$AO?.(!1),void 0===n?s=void 0:(s=new n(e),s._$AT(e,i,o)),void 0!==o?(i._$Co??=[])[o]=s:i._$Cl=s),void 0!==s&&(t=G(e,s._$AS(e,t.values),s,o)),t}class Q{constructor(e,t){this._$AV=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(e){const{el:{content:t},parts:i}=this._$AD,o=(e?.creationScope??L).importNode(t,!0);q.currentNode=o;let s=q.nextNode(),n=0,a=0,r=i[0];for(;void 0!==r;){if(n===r.index){let t;2===r.type?t=new X(s,s.nextSibling,this,e):1===r.type?t=new r.ctor(s,r.name,r.strings,this,e):6===r.type&&(t=new se(s,this,e)),this._$AV.push(t),r=i[++a]}n!==r?.index&&(s=q.nextNode(),n++)}return q.currentNode=L,o}p(e){let t=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(e,i,t),t+=i.strings.length-2):i._$AI(e[t])),t++}}class X{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(e,t,i,o){this.type=2,this._$AH=W,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=i,this.options=o,this._$Cv=o?.isConnected??!0}get parentNode(){let e=this._$AA.parentNode;const t=this._$AM;return void 0!==t&&11===e?.nodeType&&(e=t.parentNode),e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=G(this,e,t),H(e)?e===W||null==e||""===e?(this._$AH!==W&&this._$AR(),this._$AH=W):e!==this._$AH&&e!==B&&this._(e):void 0!==e._$litType$?this.$(e):void 0!==e.nodeType?this.T(e):(e=>O(e)||"function"==typeof e?.[Symbol.iterator])(e)?this.k(e):this._(e)}O(e){return this._$AA.parentNode.insertBefore(e,this._$AB)}T(e){this._$AH!==e&&(this._$AR(),this._$AH=this.O(e))}_(e){this._$AH!==W&&H(this._$AH)?this._$AA.nextSibling.data=e:this.T(L.createTextNode(e)),this._$AH=e}$(e){const{values:t,_$litType$:i}=e,o="number"==typeof i?this._$AC(e):(void 0===i.el&&(i.el=J.createElement(Z(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===o)this._$AH.p(t);else{const e=new Q(o,this),i=e.u(this.options);e.p(t),this.T(i),this._$AH=e}}_$AC(e){let t=Y.get(e.strings);return void 0===t&&Y.set(e.strings,t=new J(e)),t}k(e){O(this._$AH)||(this._$AH=[],this._$AR());const t=this._$AH;let i,o=0;for(const s of e)o===t.length?t.push(i=new X(this.O(P()),this.O(P()),this,this.options)):i=t[o],i._$AI(s),o++;o<t.length&&(this._$AR(i&&i._$AB.nextSibling,o),t.length=o)}_$AR(e=this._$AA.nextSibling,t){for(this._$AP?.(!1,!0,t);e!==this._$AB;){const t=A(e).nextSibling;A(e).remove(),e=t}}setConnected(e){void 0===this._$AM&&(this._$Cv=e,this._$AP?.(e))}}class ee{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(e,t,i,o,s){this.type=1,this._$AH=W,this._$AN=void 0,this.element=e,this.name=t,this._$AM=o,this.options=s,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=W}_$AI(e,t=this,i,o){const s=this.strings;let n=!1;if(void 0===s)e=G(this,e,t,0),n=!H(e)||e!==this._$AH&&e!==B,n&&(this._$AH=e);else{const o=e;let a,r;for(e=s[0],a=0;a<s.length-1;a++)r=G(this,o[i+a],t,a),r===B&&(r=this._$AH[a]),n||=!H(r)||r!==this._$AH[a],r===W?e=W:e!==W&&(e+=(r??"")+s[a+1]),this._$AH[a]=r}n&&!o&&this.j(e)}j(e){e===W?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,e??"")}}class te extends ee{constructor(){super(...arguments),this.type=3}j(e){this.element[this.name]=e===W?void 0:e}}class ie extends ee{constructor(){super(...arguments),this.type=4}j(e){this.element.toggleAttribute(this.name,!!e&&e!==W)}}class oe extends ee{constructor(e,t,i,o,s){super(e,t,i,o,s),this.type=5}_$AI(e,t=this){if((e=G(this,e,t,0)??W)===B)return;const i=this._$AH,o=e===W&&i!==W||e.capture!==i.capture||e.once!==i.once||e.passive!==i.passive,s=e!==W&&(i===W||o);o&&this.element.removeEventListener(this.name,this,i),s&&this.element.addEventListener(this.name,this,e),this._$AH=e}handleEvent(e){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,e):this._$AH.handleEvent(e)}}class se{constructor(e,t,i){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(e){G(this,e)}}const ne=w.litHtmlPolyfillSupport;ne?.(J,X),(w.litHtmlVersions??=[]).push("3.3.2");const ae=globalThis;class re extends x{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const e=super.createRenderRoot();return this.renderOptions.renderBefore??=e.firstChild,e}update(e){const t=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(e),this._$Do=((e,t,i)=>{const o=i?.renderBefore??t;let s=o._$litPart$;if(void 0===s){const e=i?.renderBefore??null;o._$litPart$=s=new X(t.insertBefore(P(),e),e,void 0,i??{})}return s._$AI(e),s})(t,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return B}}re._$litElement$=!0,re.finalized=!0,ae.litElementHydrateSupport?.({LitElement:re});const le=ae.litElementPolyfillSupport;le?.({LitElement:re}),(ae.litElementVersions??=[]).push("4.2.2");const ce=e=>(t,i)=>{void 0!==i?i.addInitializer(()=>{customElements.define(e,t)}):customElements.define(e,t)},de={attribute:!0,type:String,converter:$,reflect:!1,hasChanged:b},he=(e=de,t,i)=>{const{kind:o,metadata:s}=i;let n=globalThis.litPropertyMetadata.get(s);if(void 0===n&&globalThis.litPropertyMetadata.set(s,n=new Map),"setter"===o&&((e=Object.create(e)).wrapped=!0),n.set(i.name,e),"accessor"===o){const{name:o}=i;return{set(i){const s=t.get.call(this);t.set.call(this,i),this.requestUpdate(o,s,e,!0,i)},init(t){return void 0!==t&&this.C(o,void 0,e,t),t}}}if("setter"===o){const{name:o}=i;return function(i){const s=this[o];t.call(this,i),this.requestUpdate(o,s,e,!0,i)}}throw Error("Unsupported decorator location: "+o)};function pe(e){return(t,i)=>"object"==typeof i?he(e,t,i):((e,t,i)=>{const o=t.hasOwnProperty(i);return t.constructor.createProperty(i,e),o?Object.getOwnPropertyDescriptor(t,i):void 0})(e,t,i)}function ue(e){return pe({...e,state:!0,attribute:!1})}// ===== PIXELIT LIVEVIEW CARD =====
const CARD_NAME="pixelit-liveview-card";
const CARD_TYPE="custom:"+CARD_NAME;
const EDITOR_TAG=CARD_NAME+"-editor";

// ===== i18n =====
const I18N={
  de:{title:"Titel",entity:"PixelIt-Sensor",width:"Matrix-Breite (Pixel)",height:"Matrix-Höhe (Pixel)",gap:"Abstand zwischen Pixeln (px)",show_header:"Karten-Header anzeigen",show_status:"Verbindungsstatus anzeigen",show_pixels:"Pixel anzeigen",general:"Allgemein",display:"Anzeige",connected:"Verbunden",disconnected:"Getrennt",no_data:"Keine Daten",card_title:"PixelIt Liveview",pixelit_settings:"PixelIt-Einstellungen",display_options:"Anzeige-Optionen",entity_hint:"z.B. sensor.pixelit_liveview"},
  en:{title:"Title",entity:"PixelIt sensor",width:"Matrix width (pixels)",height:"Matrix height (pixels)",gap:"Gap between pixels (px)",show_header:"Show card header",show_status:"Show connection status",show_pixels:"Show pixels",general:"General",display:"Display",connected:"Connected",disconnected:"Disconnected",no_data:"No data",card_title:"PixelIt Liveview",pixelit_settings:"PixelIt settings",display_options:"Display options",entity_hint:"e.g. sensor.pixelit_liveview"}
};
function getLang(hass){const lang=(hass.locale?.language||hass.language||"en").split("-")[0];return I18N[lang]?lang:"en";}
function tr(hass,key){if(!hass)return I18N.en[key]||key;const lang=getLang(hass);return(I18N[lang]&&I18N[lang][key])||I18N.en[key]||key;}

// ===== Editor =====
let PLEditor=class extends re{
  setConfig(config){
    this._config={title:"",entity:"sensor.pixelit_liveview",width:32,height:8,gap:1,show_header:true,show_status:true,show_pixels:true,...config,type:config.type||CARD_TYPE};
  }
  _emit(){this.dispatchEvent(new CustomEvent("config-changed",{detail:{config:this._config},bubbles:true,composed:true}));}
  _patch(patch){this._config={...this._config,...patch};this._emit();}

  render(){
    if(!this._config)return V``;
    const self=this;
    const T=function(key){return tr(self.hass,key);};
    return V`<div class="editor"><div class="section-head sub"><span>${T("pixelit_settings")}</span></div><label class="text-row"><span class="text-label">${T("entity")}</span><input type="text" class="text-input" placeholder="${T("entity_hint")}" .value=${this._config.entity||""} @input=${function(e){self._patch({entity:e.target.value});}} /></label><div class="row"><label class="number-row"><span class="number-label">${T("width")}</span><input type="number" class="number-input" min="1" max="128" .value=${String(this._config.width??32)} @input=${function(e){const v=parseInt(e.target.value,10);Number.isFinite(v)&&v>0&&self._patch({width:v});}} /></label><label class="number-row"><span class="number-label">${T("height")}</span><input type="number" class="number-input" min="1" max="64" .value=${String(this._config.height??8)} @input=${function(e){const v=parseInt(e.target.value,10);Number.isFinite(v)&&v>0&&self._patch({height:v});}} /></label></div><div class="section-divider"></div><div class="section-head sub"><span>${T("display_options")}</span></div><label class="number-row"><span class="number-label">${T("gap")}</span><input type="number" class="number-input" min="0" max="16" .value=${String(this._config.gap??1)} @input=${function(e){const v=parseInt(e.target.value,10);Number.isFinite(v)&&v>=0&&self._patch({gap:v});}} /></label><label class="toggle-row"><ha-switch .checked=${this._config.show_header??true} @change=${function(e){self._patch({show_header:e.target.checked});}}></ha-switch><span>${T("show_header")}</span></label><label class="toggle-row"><ha-switch .checked=${this._config.show_status??true} @change=${function(e){self._patch({show_status:e.target.checked});}}></ha-switch><span>${T("show_status")}</span></label><label class="toggle-row"><ha-switch .checked=${this._config.show_pixels??true} @change=${function(e){self._patch({show_pixels:e.target.checked});}}></ha-switch><span>${T("show_pixels")}</span></label><div class="section-divider"></div><div class="section-head sub"><span>${T("general")}</span></div><label class="text-row"><span class="text-label">${T("title")}</span><input type="text" class="text-input" placeholder="${T("card_title")}" .value=${this._config.title||""} @input=${function(e){self._patch({title:e.target.value});}} /></label></div>`;
  }
};
PLEditor.styles=a`
.editor{padding:12px;display:flex;flex-direction:column;gap:12px;}
.section-head{display:flex;align-items:center;justify-content:space-between;font-weight:600;font-size:14px;margin-top:4px;}
.section-head.sub{font-size:13px;font-weight:500;color:var(--secondary-text-color);}
.section-divider{height:1px;background:var(--divider-color);margin:4px 0;}
.text-row{display:flex;align-items:center;justify-content:space-between;gap:12px;font-size:13px;}
.text-label{color:var(--primary-text-color);}
.text-input{flex:1;max-width:240px;padding:6px 8px;border-radius:6px;border:1px solid var(--divider-color);background:var(--card-background-color);color:var(--primary-text-color);font-size:14px;}
.text-input:focus{outline:none;border-color:var(--primary-color);}
.number-row{display:flex;align-items:center;justify-content:space-between;gap:12px;font-size:13px;}
.number-label{color:var(--primary-text-color);}
.number-input{width:80px;padding:6px 8px;border-radius:6px;border:1px solid var(--divider-color);background:var(--card-background-color);color:var(--primary-text-color);font-size:14px;text-align:right;}
.number-input:focus{outline:none;border-color:var(--primary-color);}
.row{display:flex;gap:8px;align-items:center;}
.row>*{flex:1;}
.toggle-row{display:flex;align-items:center;gap:10px;font-size:13px;cursor:pointer;padding:2px 0;}
`;
e([pe({attribute:false})],PLEditor.prototype,"hass",void 0);
e([ue()],PLEditor.prototype,"_config",void 0);
PLEditor=e([ce(EDITOR_TAG)],PLEditor);

// ===== Main Card =====
let PixelItLiveviewCard=class extends re{
  setConfig(config){if(!config)throw new Error("Invalid configuration");this._config={title:"",entity:"sensor.pixelit_liveview",width:32,height:8,gap:1,show_header:true,show_status:true,show_pixels:true,...config,type:config.type||CARD_TYPE};}
  getCardSize(){return 3;}
  getGridOptions(){return{columns:12,rows:"auto",min_columns:4,min_rows:2};}
  static getConfigElement(){return document.createElement(EDITOR_TAG);}
  static getStubConfig(hass){
    const entity=Object.values(hass?.entities??{}).find(
      entry=>entry.platform==="pixelit_liveview"&&hass.states?.[entry.entity_id]
    )?.entity_id;
    return{type:CARD_TYPE,title:"",entity:entity??"sensor.pixelit_liveview",width:32,height:8,gap:1,show_header:true,show_status:true,show_pixels:true};
  }

  shouldUpdate(changedProperties){
    if(changedProperties.has("_config")||!changedProperties.has("hass"))return true;
    const previousHass=changedProperties.get("hass");
    if(!previousHass||!this.hass)return true;
    const entity=this._config?.entity;
    return previousHass.states?.[entity]!==this.hass.states?.[entity]
      ||getLang(previousHass)!==getLang(this.hass);
  }

  _getData(){
    const entity=this._config.entity;
    if(!entity||!this.hass||!this.hass.states)return null;
    const state=this.hass.states[entity];
    if(!state)return null;
    const attrs=state.attributes||{};
    const connected=state.state==="connected";
    const hex=attrs.hex||"";
    const width=attrs.width||this._config.width||32;
    const height=attrs.height||this._config.height||8;
    const pixels=attrs.pixels||this._parseHex(hex,width,height);
    return{connected:connected,hex:hex,width:width,height:height,pixels:pixels};
  }
  _parseHex(hex,width,height){
    const pixels=[];
    const expected=width*height*6;
    const s=hex.length>=expected?hex.substring(0,expected):hex;
    for(let i=0;i<s.length;i+=6){
      const chunk=s.substring(i,i+6);
      if(chunk.length<6)break;
      const r=parseInt(chunk.substring(0,2),16);
      const g=parseInt(chunk.substring(2,4),16);
      const b=parseInt(chunk.substring(4,6),16);
      pixels.push({r:r,g:g,b:b});
    }
    return pixels;
  }

  render(){
    if(!this._config)return V``;
    const self=this;
    const T=function(key){return tr(self.hass,key);};
    const cfg=this._config;
    const data=this._getData();
    const width=data?data.width:(cfg.width||32);
    const height=data?data.height:(cfg.height||8);
    const gap=cfg.gap??1;
    const connected=data?data.connected:false;
    const statusText=connected?T("connected"):T("disconnected");
    const statusClass=connected?"ok":"err";
    const title=cfg.title||"PixelIt";
    const hasPixels=data&&data.pixels&&data.pixels.length>0;
    const gridStyle="grid-template-columns:repeat("+width+", 1fr);grid-template-rows:repeat("+height+", 1fr);gap:"+gap+"px;width:100%;";
    const cells=[];
    if(cfg.show_pixels&&data?.pixels){
      for(let y=0;y<height;y++){
        for(let x=0;x<width;x++){
          const idx=y*width+x;
          const p=data.pixels[idx];
          // Lit pixels get their real color; unlit pixels get a fully OPAQUE
          // dark fill. Semi-transparent (rgba 0.55) still lets the theme's
          // backdrop-filter blur bleed through, making unlit cells alternate
          // between black and purple depending on background position.
          // Opaque black breaks the theme bleed completely while the card
          // border/glass effect remains via the transparent .plc-inner.
          const bg=p?("rgb("+p.r+","+p.g+","+p.b+")"):"#000";
          cells.push(V`<div class="px" style="background:${bg};"></div>`);
        }
      }
    }
    return V`<ha-card class="plc"><div class="plc-inner">${cfg.show_header?V`<div class="plc-header"><span class="plc-title">${title}</span>${cfg.show_status?V`<span class="plc-status ${statusClass}">${statusText}</span>`:W}</div>`:W}${cfg.show_pixels?V`<div class="plc-grid" style="${gridStyle}">${cells}</div>`:W}${!hasPixels?V`<div class="plc-empty">${T("no_data")}</div>`:W}</div></ha-card>`;
  }
};
PixelItLiveviewCard.styles=a`
:host{--plc-bg:transparent;}
ha-card{background:transparent;box-shadow:none;border:none;}
.plc-inner{display:flex;flex-direction:column;gap:8px;padding:12px;background:var(--plc-bg);border-radius:12px;}
.plc-header{display:flex;align-items:center;justify-content:space-between;gap:8px;}
.plc-title{font-size:14px;font-weight:600;color:var(--primary-text-color);}
.plc-status{font-size:11px;padding:2px 8px;border-radius:10px;font-weight:500;}
.plc-status.ok{background:rgba(76,175,80,0.2);color:var(--success-color,#4caf50);}
.plc-status.err{background:rgba(244,67,54,0.2);color:var(--error-color,#f44336);}
.plc-grid{display:grid;width:100%;align-self:stretch;background:#000;border-radius:4px;overflow:hidden;}
.px{aspect-ratio:1/1;border-radius:1px;}
.plc-empty{font-size:12px;color:var(--secondary-text-color);padding:8px 0;}
`;
e([pe({attribute:false})],PixelItLiveviewCard.prototype,"hass",void 0);
e([ue()],PixelItLiveviewCard.prototype,"_config",void 0);
PixelItLiveviewCard=e([ce(CARD_NAME)],PixelItLiveviewCard);

window.customCards=window.customCards||[];
window.customCards.push({type:CARD_NAME,name:"PixelIt Liveview",description:"Zeigt den aktuellen Inhalt eines PixelIt-Displays (über HA-Sensor)",preview:false,configurable:true,show_form_editors:true});
export{PixelItLiveviewCard as PixelItLiveviewCard};
