// This function erases the canvas content and resets canvas size.
const clear = () => {
	const canvas = document.getElementById('draw');
	canvas.width = canvas.clientWidth;
	canvas.height = canvas.clientHeight;
}

// This function draws the graph on the canvas.
const draw = () => {
	
	// Important elements and objects.
	const canvas = document.getElementById('draw');
	const tickers = document.getElementById('tickers');
	const istart = document.getElementById('range_start');
	const ifinish = document.getElementById('range_finish');
	const ctx = canvas.getContext('2d');
	
	// Clear canvas.
	clear();
	
	// Radius of points, caption font size and style.
	const pts_radius = Math.floor(PTS_RADIUS_PERCENT / 100 * Math.min(canvas.width, canvas.height)) + 1;
	const font_size = pts_radius * FONT_ENLARGEMENT;
	ctx.font = `${FONT_MOD} ${font_size}px ${FONT_NAME}`;
	ctx.textBaseline = 'middle'; //to count height_offset properly later
	
	// Generate request string, considering rules as follows:
	// -- by default, get last ticker pts in a default window range;
	// -- if any range input field is in focus and range is correct,
	// get ticker pts info based on specified range;
	// -- active ticker is included into request (default value is 1).
	const select_ticker = tickers.value === '' ? 1 : tickers.value;
	const in_focus = [istart, ifinish].includes(document.activeElement);
	let fetch_req;
	if (in_focus) {
		const start_range = parseInt(istart.value);
		const finish_range = parseInt(ifinish.value);
		if (!isNaN(start_range) && !isNaN(finish_range))
			fetch_req = `summary/${select_ticker}/${start_range}/${finish_range}`;
	}
	if (fetch_req === undefined)
		fetch_req = `summary/${select_ticker}/${TICKERS_WINDOW}`;

	// Gathering info from server.
	fetch(fetch_req)
	.then(response => response.json())
	.then((response) => {
		
		// Processing pts values.
		const pts = response.values;
		const minpts = Math.min(...pts);
		const maxpts = Math.max(...pts);
		const divider = maxpts - minpts;
		const pts_count = pts.length;

		// Update range data if range input fields
		// are not in focus.
		if (!in_focus) {
			const pts_start = response.start;
			const pts_finish = response.finish;
			istart.value = pts_start;
			ifinish.value = pts_finish;
		}
		
		// Pts normalization, considering reverted axis.
		const normalized_pts = pts.map((elem) => (divider === 0) ? 1 : 1 - ((elem - minpts) / divider));
		
		// Width and height of real graph workspace.
		const workspace_w = canvas.width - HORIZONTAL_MARGIN * 2;
		const workspace_h = canvas.height - VERTICAL_MARGIN * 2;		
		if ((workspace_w <= 0) || (workspace_h <= 0)) {
			console.error("No space to show");
		} else {			
			// Map [0..1] normalized pts range to real pixels.
			const pixels = normalized_pts.map((elem, index) => [
				Math.trunc(index / (pts_count - 1) * workspace_w + HORIZONTAL_MARGIN),
				Math.trunc(elem * workspace_h + VERTICAL_MARGIN)
			]);
			
			// Prepare to draw.
			ctx.fillStyle = COLOR_OBJECT;
			ctx.strokeStyle = COLOR_OBJECT;
			
			// Layer 1: Polyline.
			pixels.forEach((elem, index) => {				
				const [x, y] = elem;
				if (index === 0) {
					ctx.moveTo(x, y);
				} else {
					ctx.lineTo(x, y);
					ctx.stroke();
				}
			});
			
			// Layer 2: Circles (pts) and caption.											
			pixels.forEach((elem, index) => {
				const [x, y] = elem;
				const caption = pts[index];
				ctx.beginPath();
				ctx.arc(x, y, pts_radius, 0, PI2, false);
				ctx.fill();
				
				// Prepare caption output, centering caption to the point.
				const measure_caption = ctx.measureText(caption);
				const width_offset = x - font_size + Math.trunc(measure_caption.width / 2);				
				const height_offset = measure_caption.actualBoundingBoxAscent + measure_caption.actualBoundingBoxDescent;
				
				// By default, draw the caption *below* the point;
				// if there's no room, draw above.
				const side = ((y + pts_radius) >= (canvas.height - VERTICAL_MARGIN)) ? -1 : 1;
				
				ctx.fillText(caption, width_offset, y + side * (pts_radius + height_offset + 1));
			});
			
		}
	})
	.catch((err) => {
		console.error('Can not parse array:');
		console.error(err);
	});
	
}
