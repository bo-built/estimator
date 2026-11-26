document.addEventListener('alpine:init', () => {
    Alpine.data('dashboardApp', () => ({
        catalogue: [],
        catalogueLoaded: false,
        editItem: null,
        editDraft: {},
        hasErrors: false,

        setEditItem(item) {
            this.hasErrors = false;
            this.editItem = item;
            this.editDraft = { ...item };
        },

        cancelEditItem(item) {
            this.hasErrors = false;
            //Object.assign(this.editItem, this.editDraft);
            this.editItem = null;
        },

        async saveEditItem(item) {
            this.hasErrors = false;
            this.hasErrors = this.checkForErrors();
            if(!this.hasErrors) {
                try {
                    var payload = this.editDraft;
                    const response = await fetch(this.editDraft.api_url, {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken'),
                        },
                        body: JSON.stringify(payload),
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        console.error('Validation errors:', data);
                        return;
                    } else {
                        Object.assign(this.editItem, this.editDraft);
                        this.editItem = null;
                    }
                }  catch (error) {
                    console.error('Failed to update item:', error);
                }
            } else {
                return;
            }
        },

        updateEditDraftChargeRate() {
            this.editDraft.charge_rate = this.editDraft.cost_rate * this.editDraft.charge_multiplier;
        },

        nameIsDuplicate() {
            const draftName = this.editDraft.name?.trim().toLowerCase();
            if (!draftName) return false;

            return this.catalogue.some(item =>
                item.pk !== this.editDraft.pk &&
                item.name?.trim().toLowerCase() === draftName
            );
        },

        skuIsDuplicate() {
            const draftSku = this.editDraft.sku?.trim().toLowerCase();
            if (!draftSku) return false;

            return this.catalogue.some(item =>
                item.pk !== this.editDraft.pk &&
                item.sku?.trim().toLowerCase() === draftSku
            );
        },

        validNumber(val) {
            return val !== null &&
            String(val).trim() !== "" &&
            Number.isFinite(Number(val)) &&
            Number(val) > 0
        },

        checkForErrors() {
            if(!this.editDraft.name?.trim()) {
                return true;
            }
            if(!this.editDraft.sku?.trim()) {
                return true;
            }
            if(this.nameIsDuplicate() || this.skuIsDuplicate()) {
                return true;
            }
            if(!this.validNumber(this.editDraft.cost_rate) || !this.validNumber(this.editDraft.charge_multiplier)) {
                return true;
            }
            return false;
        },

        async initDashoard(fetch_url) {
            // Fetch the material type catalogue
            try {
                const response = await fetch(fetch_url);
                this.catalogue = await response.json();
            } catch (error) {
                console.error('Error fetching catalogue data:', error);
            } finally {
                this.catalogueLoaded = true;
            }
        }
    }));
});