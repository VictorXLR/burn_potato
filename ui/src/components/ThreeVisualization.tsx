import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

interface ThreeVisualizationProps {
  data: number[];
}

const ThreeVisualization: React.FC<ThreeVisualizationProps> = ({ data }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const pointsRef = useRef<THREE.Points | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Setup scene
    const scene = new THREE.Scene();
    sceneRef.current = scene;
    scene.background = new THREE.Color(0x000000);

    // Setup camera
    const camera = new THREE.PerspectiveCamera(
      75,
      containerRef.current.clientWidth / containerRef.current.clientHeight,
      0.1,
      1000
    );
    cameraRef.current = camera;
    camera.position.z = 5;

    // Setup renderer
    const renderer = new THREE.WebGLRenderer();
    rendererRef.current = renderer;
    renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight);
    containerRef.current.appendChild(renderer.domElement);

    // Add controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // Cleanup
    return () => {
      renderer.dispose();
      containerRef.current?.removeChild(renderer.domElement);
    };
  }, []);

  useEffect(() => {
    if (!sceneRef.current || !data.length) return;

    // Remove existing points
    if (pointsRef.current) {
      sceneRef.current.remove(pointsRef.current);
    }

    // Create points geometry
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(data.length * 3);
    const colors = new Float32Array(data.length * 3);

    for (let i = 0; i < data.length; i++) {
      const value = data[i];
      positions[i * 3] = (i % 100) / 50 - 1; // x
      positions[i * 3 + 1] = Math.floor(i / 100) / 50 - 1; // y
      positions[i * 3 + 2] = value / 255; // z

      // Color based on value
      colors[i * 3] = value / 255;
      colors[i * 3 + 1] = 0.5;
      colors[i * 3 + 2] = 1.0 - (value / 255);
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.01,
      vertexColors: true
    });

    const points = new THREE.Points(geometry, material);
    pointsRef.current = points;
    sceneRef.current.add(points);
  }, [data]);

  return <div ref={containerRef} style={{ width: '100%', height: '100vh' }} />;
};

export default ThreeVisualization;