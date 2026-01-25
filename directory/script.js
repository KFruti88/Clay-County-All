let masterData = [];

// 1. PROJECT CONFIGURATION
const imageRepo = "https://raw.githubusercontent.com/KFruti88/images/main/";
const csvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRDgQs5fH6y8PWw9zJ7_3237SB2lxlsx8Gnw8o8xvTr94vVtWwzs6qqidajKbPepQDS36GNo97bX_4b/pub?gid=0&single=true&output=csv";
const couponImg = "https://raw.githubusercontent.com/KFruti88/images/main/Coupon.png";

// Shared brands that use one logo for multiple towns
const sharedBrands = ["casey's", "mcdonald's", "huck's", "subway", "dollar general", "mach 1"];

const catEmojis = {
    "Emergency": "🚨", "Manufacturing": "🏗️", "Bars": "🍺", "Professional Services": "💼",
    "Financial Services": "💰", "Retail": "🛒", "Shopping": "🛍️", "Restaurants": "🍴",
    "Church": "⛪", "Post Office": "📬", "Healthcare": "🏥", "Support Services": "🛠️",
    "Internet": "🌐", "Gas Station": "⛽", "Industry": "🏭", "Agriculture": "🚜"
};

// 2. INITIALIZATION
document.addEventListener("DOMContentLoaded", () => {
    updateNewspaperHeader();
    loadDirectory();
});

// 3. NEWSPAPER HEADER LOGIC
function updateNewspaperHeader() {
    const now = new Date();
    const dateOptions = { month: 'long', day: 'numeric', year: 'numeric' };
    const dateString = now.toLocaleDateString('en-US', dateOptions);
    const headerElement = document.getElementById('header-info');
    if(headerElement) {
        headerElement.innerText = `VOL. 1 — NO. ${now.getMonth() + 1} | ${dateString}`;
    }
}

// 4. SMART IMAGE HELPER
function getSmartImage(id, bizName, isProfile = false) {
    if (!id && !bizName) return `https://via.placeholder.com/${isProfile ? '250' : '150'}?text=Logo+Pending`;
    
    let fileName = id.trim().toLowerCase();
    const nameLower = bizName ? bizName.toLowerCase() : "";

    const brandMatch = sharedBrands.find(brand => nameLower.includes(brand));
    if (brandMatch) {
        fileName = brandMatch.replace(/['\s]/g, ""); 
    }

    const placeholder = `https://via.placeholder.com/${isProfile ? '250' : '150'}?text=Logo+Pending`;
    const firstUrl = `${imageRepo}${fileName}.jpg`;
    
    return `<img src="${firstUrl}" 
            class="${isProfile ? 'profile-logo' : ''}" 
            onerror="this.onerror=null; 
            this.src='${imageRepo}${fileName}.png'; 
            this.onerror=function(){this.src='${placeholder}'};">`;
}

// 5. DATA LOADING ENGINE
async function loadDirectory() {
    Papa.parse(csvUrl, {
        download: true, header: true, skipEmptyLines: true,
        complete: (results) => {
            masterData = results.data.filter(row => row.Name && row.Name.trim() !== "");
            
            // Detect which page is active and render accordingly
            if (document.getElementById('directory-grid')) {
                renderCards(masterData);
            } else if (document.getElementById('profile-wrap')) {
                loadProfile(masterData);
            }
        }
    });
}

// 6. RENDER MAIN DIRECTORY
function renderCards(data) {
    const grid = document.getElementById('directory-grid');
    if (!grid) return;

    // Sorting: Premium -> Plus -> Basic
    const tierOrder = { "premium": 1, "plus": 2, "basic": 3 };

    grid.innerHTML = data.sort((a, b) => {
        const tierA = (a.Teir || 'basic').toLowerCase();
        const tierB = (b.Teir || 'basic').toLowerCase();
        if (tierOrder[tierA] !== tierOrder[tierB]) return tierOrder[tierA] - tierOrder[tierB];
        return (a.Town || "").localeCompare(b.Town || "");
    }).map(biz => {
        const tier = (biz.Teir || 'basic').toLowerCase();
        const hasCoupon = biz.Coupon && biz.Coupon !== "N/A" && biz.Coupon.trim() !== "";
        const townClass = (biz.Town || "unknown").toLowerCase().replace(/\s+/g, '-');
        const imageID = (biz['Image ID'] || "").trim();
        const category = (biz.Category || "Industry").trim();

        // Click Logic
        let clickAttr = "";
        if (tier === 'premium') {
            clickAttr = `onclick="window.location.href='profile.html?id=${encodeURIComponent(imageID.toLowerCase())}'"`;
        } else if (tier === 'plus') {
            clickAttr = `onclick="this.classList.toggle('expanded')"`;
        }

        return `
            <div class="card ${tier}" ${clickAttr} style="cursor: ${tier !== 'basic' ? 'pointer' : 'default'};">
                <div class="tier-badge">${tier}</div>
                ${hasCoupon ? `<img src="${couponImg}" class="coupon-badge" alt="Discount Available">` : ''}
                <div class="logo-box">${getSmartImage(imageID, biz.Name)}</div>
                <div class="town-bar ${townClass}-bar">${biz.Town || 'Unknown'}</div>
                <h2 style="font-size: 1.4rem; margin: 5px 0; line-height: 1.1;">${biz.Name}</h2>
                
                ${tier === 'plus' ? `
                    <div class="plus-reveal">
                        <p><strong>Phone:</strong> ${biz.Phone || 'N/A'}</p>
                        <p><strong>Est:</strong> ${biz['Date Started'] || 'N/A'}</p>
                    </div>` : ''}

                <div style="margin-top: auto; font-style: italic; font-size: 0.85rem; color: #444;">
                    ${catEmojis[category] || "📁"} ${category}
                </div>
            </div>`;
    }).join('');
}

// 7. PROFILE PAGE ENGINE
function loadProfile(data) {
    const params = new URLSearchParams(window.location.search);
    const bizId = params.get('id');
    const wrap = document.getElementById('profile-wrap');
    if (!bizId || !wrap) return;

    const biz = data.find(b => b['Image ID'].trim().toLowerCase() === bizId.toLowerCase());
    if (!biz) {
        wrap.innerHTML = `<div style="text-align:center;"><h2>Business Not Found</h2><a href="index.html">Back to Directory</a></div>`;
        return;
    }

    const hasCoupon = biz.Coupon && biz.Coupon !== "N/A" && biz.Coupon.trim() !== "";
    const category = biz.Category || "Industry";

    wrap.innerHTML = `
        <div class="profile-container">
            <div class="tier-indicator">${biz.Teir} Member</div>
            <a href="index.html" class="back-link">← BACK TO DIRECTORY</a>
            <div class="profile-header">
                <div class="profile-logo-box">${getSmartImage(biz['Image ID'], biz.Name, true)}</div>
                <div>
                    <h1 class="biz-title">${biz.Name}</h1>
                    <p class="biz-meta">${catEmojis[category] || "📂"} ${category} | ${biz.Town}</p>
                    <p class="biz-meta"><strong>Established:</strong> ${biz['Date Started'] || 'N/A'}</p>
                </div>
            </div>
            <div class="details-grid">
                <div class="info-section">
                    <h3>Contact Information</h3>
                    <div class="info-item"><strong>📞 Phone:</strong> ${biz.Phone}</div>
                    <div class="info-item"><strong>📍 Address:</strong><br>${biz.Address || 'Contact for location'}</div>
                    ${biz.Website ? `<a href="${biz.Website}" target="_blank" class="action-btn">Visit Website</a>` : ''}
                    ${biz.Facebook ? `<br><a href="${biz.Facebook}" target="_blank" style="display:inline-block; margin-top:10px; color:#3b5998; font-weight:bold; text-decoration:none;">Find us on Facebook</a>` : ''}
                </div>
                <div class="info-section">
                    <h3>Member Specials</h3>
                    ${hasCoupon ? `<div style="background:#fff; border:2px dashed #000; padding:15px; text-align:center;"><img src="${couponImg}" style="width:80px; margin-bottom:10px;"><p style="margin:0; font-weight:bold;">Special Offer Available!</p><small>Mention SMLC to redeem.</small></div>` : '<p>No current coupons available.</p>'}
                </div>
            </div>
            ${biz.Bio ? `<div class="info-section" style="margin-top:30px;"><h3>About Our Business</h3><div class="bio-box">${biz.Bio}</div></div>` : ''}
            ${biz.Address ? `<div class="info-section" style="margin-top:30px;"><h3>Location</h3><div class="map-box"><iframe width="100%" height="100%" frameborder="0" style="border:0" src="https://maps.google.com/maps?q=${encodeURIComponent(biz.Address + " " + (biz.Town || "") + " IL")}&output=embed" allowfullscreen></iframe></div></div>` : ''}
        </div>`;
}

// 8. FILTER LOGIC
function applyFilters() {
    const t = document.getElementById('town-select').value;
    const c = document.getElementById('cat-select').value;
    const filtered = masterData.filter(b => (t === 'All' || b.Town === t) && (c === 'All' || b.Category === c));
    renderCards(filtered);
}

function resetFilters() {
    document.getElementById('town-select').value = 'All';
    document.getElementById('cat-select').value = 'All';
    renderCards(masterData);
}
