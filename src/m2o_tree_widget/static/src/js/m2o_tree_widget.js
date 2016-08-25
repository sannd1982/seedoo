    openerp.m2o_tree_widget = function(instance)
 {

    var QWeb = instance.web.qweb;
    var _t = instance.web._t;
    var _lt = instance.web._lt;
     instance.m2o_tree_widget.FieldMany2OneTree = instance.web.form.AbstractField.extend(instance.web.form.ReinitializeFieldMixin,{
        template: 'm2o_tree',
        init: function(field_manager, node) {
            this._super(field_manager, node);
            this.is_started = false;
        },
        reinit_value: function(val) {
            this.internal_set_value(val);
            this.floating = false;
            if (this.is_started && !this.no_rerender)
            		this.render_value(true);
        },
        initialize_field: function() {
            this.is_started = true;
            instance.web.form.ReinitializeFieldMixin.initialize_field.call(this);
        },
        initialize_content: function() {
            if (!this.get("effective_readonly"))
                this.render_editable();
        },
        render_value: function(no_recurse) {
            var self = this;
            if (! this.get("value")) {
                this.display_string("");
                return;
            }
            var display = false;
            if (this.display_value) {
            	display = this.display_value["" + this.get("value")];
            }
            if (display) {
                this.display_string(display);
                return;
            }
            if (! no_recurse) {
                var dataset = new instance.web.DataSetStatic(this, this.field.relation, self.build_context());
                var def = this.alive(dataset.name_get([self.get("value")])).done(function(data) {
                    if (!data[0]) {
                        self.do_warn(_t("Render"), _t("No value found for the field "+self.field.string+" for value "+self.get("value")));
                        return;
                    }
                    self.display_value["" + self.get("value")] = data[0][1];
                    self.render_value(true);
                });
                if (this.view && this.view.render_value_defs){
                    this.view.render_value_defs.push(def);
                }
            }
        },
        display_string: function(str) {
            var self = this;
            if (this.get("effective_readonly")) {
                var lines = _.escape(str).split("\n");
                var link = "";
                var follow = "";
                link = lines[0];
                follow = _.rest(lines).join("<br />");
                if (follow)
                    link += "<br />";
                var $link = this.$el.find('.oe_form_uri')
                     .unbind('click')
                     .html(link);
                if (! this.options.no_open)
                    $link.click(function () {
                        self.do_action({
                            type: 'ir.actions.act_window',
                            res_model: self.field.relation,
                            res_id: self.get("value"),
                            views: [[false, 'form']],
                            target: 'current',
                            context: self.build_context().eval(),
                        });
                        return false;
                     });
                $(".oe_form_m2o_follow", this.$el).html(follow);
            }
            else {
                this.render_editable();
            }
        },
        render_editable: function() {
            var self = this;

            //this.$input = this.$el.find("input");

            var dataset = new instance.web.DataSet(this, this.field.relation, self.build_context());
            var fields = _.keys(self.fields);
            var modelFields = ['id', 'name'];
            var pid = 'parent_id';
            if (self.options.parent_field) {
            	pid = self.options.parent_field;
            }
        	modelFields.push(pid);
            var zNodes = new instance.web.Model(self.field.relation).query(modelFields)
	            .filter([])
	            .limit(300)
	            .all().then(function (res) {
	            	var zNodes = [];
	            	for (r in res) {
	            		zNodes.push(
	            				{
	            					id: res[r]['id'],
	            					pId: res[r][pid] && res[r][pid][0] || false,
	            					name: res[r]['name'],
	            					doCheck: true,
	            					checked: self.get("value") == res[r]['id'] && true || false,
	            					open: false
	            				}
	            		);
	            	}
	                var setting = {
	            			view: {
	            				selectedMulti: false
	            			},
	            			check: {
	            				enable: true,
	            				chkStyle: "radio",
	            				radioType: "all"
	            			},
	            			data: {
	            				simpleData: {
	            					enable: true
	            				}
	            			},
	            			callback: {
	            				beforeCheck: beforeCheck,
	            				onCheck: onCheck
	            			}
	            		};
    		 		var code, log, className = "dark";
    		 		function beforeCheck(treeId, treeNode) {
    		 			return (treeNode.doCheck !== false);
    		 		};
    		 		function onCheck(e, treeId, treeNode) {
    		 			
    		 			self.set_value(treeNode['id']);
    		 		};
    		 		function expandParentNode(zTree, node) {
    		 			var pnode = false;
    		 			if (node) {
    		 				pnode = zTree.getNodeByParam("id", node['pId'], null);
    		 			}
    		 			if (pnode) {
    		 				zTree.expandNode(pnode, true, true, true);
    		 				expandParentNode(zTree, pnode);
    		 			}
    		 		};
    		 		
    				$.fn.zTree.init($("#treeData"), setting, zNodes);
    				
		 			var zTree = $.fn.zTree.getZTreeObj("treeData");
		 			var nodes = zTree.getNodes();
		 			if (! self.options.all_checkable) {
			 			for (n in nodes) {
			 				if (nodes[n].isParent) {
			 					zTree.setChkDisabled(nodes[n], true);
			 				}
			 			}
		 			}
		 			var checked = zTree.getNodeByParam("checked", true, null);
		 			expandParentNode(zTree, checked);
	            });
        },
        set_value: function(value_) {
            var self = this;
            if (value_ instanceof Array) {
                this.display_value = {};
                if (! this.options.always_reload) {
                    this.display_value["" + value_[0]] = value_[1];
                }
                value_ = value_[0];
            }
            value_ = value_ || false;
            this.reinit_value(value_);
        },
    });

 instance.web.form.widgets.add('m2o_tree', 'instance.m2o_tree_widget.FieldMany2OneTree');
};
