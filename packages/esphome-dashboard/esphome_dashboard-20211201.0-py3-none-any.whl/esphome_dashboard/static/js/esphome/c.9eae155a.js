import{_ as o,e as t,t as e,n as s,a as i,y as r,J as c}from"./index-638c7e8b.js";import"./c.1a8ec74e.js";import{o as n}from"./c.5529c327.js";import"./c.c0ffde54.js";import"./c.801aca91.js";import"./c.ded24c31.js";let a=class extends i{render(){return r`
      <esphome-process-dialog
        .heading=${`Logs ${this.configuration}`}
        .type=${"logs"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":r`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){c(this.configuration)}_handleProcessDone(o){this._result=o.detail}_handleRetry(){n(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],a.prototype,"configuration",void 0),o([t()],a.prototype,"target",void 0),o([e()],a.prototype,"_result",void 0),a=o([s("esphome-logs-dialog")],a);
