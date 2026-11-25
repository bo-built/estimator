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

        saveEditItem(item) {
            this.hasErrors = false;
            Object.assign(this.editItem, this.editDraft);
            this.editItem = null;
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

        checkForErrors() {
            if(!this.editDraft.name?.trim()) {
                return true;
            }
            if(this.nameIsDuplicate() || this.skuIsDuplicate()) {
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