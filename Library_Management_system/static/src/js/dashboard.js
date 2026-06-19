/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class LibraryDashboard extends Component {

    setup() {

        this.orm = useService("orm");

        this.state = useState({

            total_books: 0,
            total_members: 0,
            issued_books: 0,
            overdue_books: 0,

            recent_issues: [],
            overdue_data: [],
        });

        onWillStart(async () => {

            const result = await this.orm.call(
                "library.dashboard",
                "get_dashboard_data",
                []
            );

            Object.assign(this.state, result);

        });
    }
}

LibraryDashboard.template = "library_dashboard_template";

registry.category("actions").add(
    "library_dashboard",
    LibraryDashboard
);