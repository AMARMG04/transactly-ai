export default function Skeleton({ height }: { height: number }) {
  return (
    <div
      className="skeleton w-full"
      style={{ height, borderRadius: 8 }}
    />
  );
}