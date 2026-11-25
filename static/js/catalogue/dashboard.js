document.addEventListener('alpine:init', () => {
    Alpine.data('dashboardApp', () => ({
        materialCatalogue: [],
        laborCatalogue: [],

        async initDashoard(materials_fetch_url, labor_fetch_url) {
            try {
                const response = await fetch(shop_api_url);
                this.shop = await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                this.fetchMachines();
                this.fetchToDoSchedule();
                this.fetchThisUser();
            }
        }
    }));
});